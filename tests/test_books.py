import datetime
import html
from flask import url_for

from foss_library.exceptions import OutOfStockError, OutstandingDuesError
from foss_library.books.models import Book
from foss_library.members.models import Member
from foss_library.books.forms import CreateBookForm, UpdateBookForm
from .base import BaseTest



class BaseBooksTestCase(BaseTest):
    def setUp(self):
        super().setUp()

        self.test_book_1 = Book.create(
            **{
                "isbn": "1400052920",
                "isbn13": "9781400052929",
                "authors": "Douglas Adams",
                "language_code": "eng",
                "ratings_count": 4930,
                "text_reviews_count": 460,
                "publisher_name": "Crown",
                "rent_per_day": 1,
                "updated_at": datetime.datetime(2021, 9, 10, 14, 25, 13, 532096),
                "id": 14,
                "title": "The Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy  #1)",
                "average_rating": 4.22,
                "num_pages": 215,
                "publication_date": datetime.datetime(2004, 8, 3, 0, 0),
                "total_stock": 1,
            }
        )

        # very expensive book
        self.test_book_2 = Book.create(
            **{
                "isbn": "0441328008",
                "isbn13": "9780441328000",
                "authors": "Frank Herbert",
                "language_code": "eng",
                "ratings_count": 45388,
                "text_reviews_count": 644,
                "publisher_name": "Ace Books",
                "rent_per_day": 250,
                "updated_at": datetime.datetime(2021, 9, 10, 14, 34, 40, 671296),
                "title": "Heretics of Dune (Dune Chronicles #5)",
                "id": 117,
                "average_rating": 3.86,
                "num_pages": 471,
                "publication_date": datetime.datetime(1987, 8, 15, 0, 0),
                "total_stock": 10,
                "created_at": datetime.datetime(2021, 9, 10, 14, 34, 40, 671296),
            }
        ) 

        self.test_member_1 = Member.create(**{"name": "test name", "email": "test@example.com"})

        self.test_book_3_kwargs = {
            "isbn": "1234567890",
            "isbn13": "1234567890123",
            "authors": "Test Author",
            "language_code": "eng",
            "publisher_name": "Crown",
            "rent_per_day": 1,
            "title": "The Hitchhiker's Tests",
            "num_pages": 215,
            "publication_date": datetime.date(2004, 8, 3),
            "total_stock": 1,
        }


class TestBookModel(BaseBooksTestCase):
    def test_book_unreturned_stock(self):
        self.assertEqual(self.test_book_1.unreturned_stock, 0)
        self.assertEqual(self.test_book_1.available_stock, 1)

        self.test_book_1.issue_to(self.test_member_1)

        self.assertEqual(self.test_book_1.unreturned_stock, 1)
        self.assertEqual(self.test_book_1.available_stock, 0)

    def test_book_out_of_stock_error(self):
        # issue once
        self.test_book_1.issue_to(self.test_member_1)

        with self.assertRaises(OutOfStockError):
            self.test_book_1.issue_to(self.test_member_1)

    def test_book_outstanding_dues_error_when_dues_greater_than_500(self):
        transaction = self.test_book_2.issue_to(self.test_member_1)

        # normal issual works
        self.test_book_1.issue_to(self.test_member_1)

        # now change borrowed_at to some old time so that the dues increase to >500
        transaction.borrowed_at -= datetime.timedelta(days=3)
        transaction.save()

        # now dues should be ~750 Rs, next issual shouldn't work
        with self.assertRaises(OutstandingDuesError):
            self.test_book_2.issue_to(self.test_member_1)

    def test_book_should_pass_when_large_dues_paid(self):
        transaction = self.test_book_2.issue_to(self.test_member_1)

        # normal issual works
        self.test_book_1.issue_to(self.test_member_1)

        # now change borrowed_at to some old time so that the dues increase to >500
        transaction.borrowed_at -= datetime.timedelta(days=3)
        transaction.save()

        # dues paid now
        transaction.return_book_and_pay_dues()

        self.test_book_2.issue_to(self.test_member_1)

class TestBookViewListBooks(BaseBooksTestCase):
    def test_list_books(self):
        response = self.client.get(url_for("books.list_books"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(html.escape("Hitchhiker").encode(), response.data)
        self.assertIn(html.escape("Frank Herbert").encode(), response.data)

    def test_list_books_with_author(self):
        response = self.client.get(url_for("books.list_books", author="douglas"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(html.escape("Hitchhiker").encode(), response.data)
        self.assertNotIn(html.escape("Frank Herbert").encode(), response.data)

    def test_list_books_with_title(self):
        response = self.client.get(url_for("books.list_books", title="Dune"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(html.escape("Frank Herbert").encode(), response.data)
        self.assertNotIn(html.escape("Hitchhiker").encode(), response.data)


class TestBookViewCreateBook(BaseBooksTestCase):
    def test_create_book_valid(self):
        test_book_3 = Book(**self.test_book_3_kwargs)
        create_form = CreateBookForm(obj=test_book_3)

        response = self.client.post(url_for("books.create_book"), data=create_form.data)

        self.assertIn(response.status_code, range(200, 400))

        test_book_from_db = Book.query.filter_by(isbn=test_book_3.isbn).first()
        self.assertIsNotNone(test_book_from_db)
