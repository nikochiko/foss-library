import asyncio
import os
from math import ceil
from pprint import pprint
from typing import Any, AsyncIterator, Optional

import aiohttp

from foss_library.books.models import Book


FRAPPE_API_URL = os.getenv(
    "FRAPPE_API_URL", "https://frappe.io/api/method/frappe-library"
)


async def get_n_books_from_api(
    count: int,
    title: Optional[str] = None,
    authors: Optional[str] = None,
    isbn: Optional[str] = None,
    publisher: Optional[str] = None,
):
    n_pages = ceil(count / 20)

    params = {
        "title": title,
        "authors": authors,
        "isbn": isbn,
        "publisher": publisher,
    }

    sent_count = 0

    async with aiohttp.ClientSession() as session:
        async for json_book in fetch_n_pages_concurrently(session, n_pages, params):
            if sent_count >= count:
                break

            book_obj = convert_json_to_book(json_book)
            sent_count += 1
            yield book_obj


async def fetch_n_pages_concurrently(
    session: aiohttp.ClientSession,
    pages: int,
    params: Optional[dict[str, Any]],
    offset: Optional[int] = 0,
) -> AsyncIterator[dict[str, Any]]:
    """
    Fetches data from API in batches. Downloading is done
    concurrently for the requests within each batch.
    """
    start_page = offset + 1
    end_page = start_page + pages
    print(f"Fetching pages {start_page} to {end_page}")
    awaitables = [
        get_data_by_page(session, page, params) for page in range(start_page, end_page)
    ]

    # gets a coroutines as they complete
    for coroutine in asyncio.as_completed(awaitables):
        json_books = await coroutine
        for json_book in json_books:
            yield json_book


async def get_data_by_page(
    session: aiohttp.ClientSession,
    page: int,
    params: Optional[dict[str, Any]] = {},
) -> list[dict[str, Any]]:
    """
    Get data from the API for a given page

    session is expected as the first argument to make use of connection pooling
    """
    params = params.copy()

    params.update(page=page)
    async with session.get(
        FRAPPE_API_URL, params=params, raise_for_status=True
    ) as response:
        response_data = await response.json()

    return response_data["message"]


def convert_json_to_book(json_book: dict[str, Any]) -> Book:
    """Converts a JSON dict (as per return format of API) to a Book object"""
    # a mapping of keys from API response to the keys that should go in as kwargs to Book
    cleanup_str_func = lambda x: str(x.strip())
    converted_keys_and_cleanup_funcs = {
        "bookID": ("id", int),
        "title": ("title", cleanup_str_func),
        "authors": ("authors", cleanup_str_func),
        "average_rating": ("average_rating", float),
        "isbn": ("isbn", cleanup_str_func),
        "isbn13": ("isbn13", cleanup_str_func),
        "language_code": ("language_code", cleanup_str_func),
        "num_pages": ("num_pages", int),
        "ratings_count": ("ratings_count", int),
        "text_reviews_count": ("text_reviews_count", int),
        "publication_date": ("publication_date", cleanup_str_func),
        "publisher": ("publisher_name", cleanup_str_func),
    }

    # new dict for kwargs to be passed to Book()
    kwargs = {}
    for key in json_book:
        # some keys have extra spaces
        cleaned_key = key.strip()

        if cleaned_key not in converted_keys_and_cleanup_funcs:
            # this should alert us
            raise Exception(f"Unexpected key found: '{key}'")

        # get new converted key and assign it in the kwargs dict
        kwargs_key, cleanup_func = converted_keys_and_cleanup_funcs[cleaned_key]
        try:
            kwargs[kwargs_key] = cleanup_func(json_book[key])
        except ValueError as e:
            print(f"Got ValueError: {e} for following JSON. Skipping")
            pprint(json_book)
            return

    return Book(**kwargs)
