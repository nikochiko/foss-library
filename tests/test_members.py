import datetime
import html

from flask import url_for

from foss_library.books.models import Book
from foss_library.members.models import Member
from .base import BaseTest


class MemberBaseTestCase(BaseTest):
    def setUp(self):
        super().setUp()

        self.member = Member.create(
            name="test",
            email="test@example.com",
        )
        self.member_2 = Member.create(
            name="test_2",
            email="test_2@example.com",
        )

        self.book = Book.create(
            title="Test Book",
            isbn="1234567890",
            isbn13="1234567890123",
            num_pages=123,
            language_code="eng",
            publication_date="2020-01-01",
            publisher_name="Test Publisher",
            total_stock=1,
            rent_per_day=1,
        )

        self.very_expensive_book = Book.create(
            title="Very expensive book",
            isbn="0101010101",
            isbn13="0101010101010",
            num_pages=101,
            language_code="en-US",
            publication_date="2007-03-14",
            publisher_name="Test Publisher",
            total_stock=1,
            rent_per_day=100,
        )

        self.valid_member_kwargs = {
            "name": "Test Member Create",
            "email": "test_member_create@example.com",
        }

        self.invalid_member_kwargs = {
            "name": "Test Member Create",
            "email": "invalid_email_with_no_domain@",
        }


class TestMemberModel(MemberBaseTestCase):
    def test_member_outstanding_dues(self):
        self.assertEqual(self.member.outstanding_dues, 0)

        transaction = self.book.issue_to(self.member)

        self.assertEqual(self.member.outstanding_dues, 0)

        transaction.update(
            borrowed_at=transaction.borrowed_at - datetime.timedelta(days=2)
        )

        expected_dues = 2 * self.book.rent_per_day

        self.assertEqual(self.member.outstanding_dues, expected_dues)

        transaction.return_book_and_pay_dues()

        self.assertEqual(self.member.outstanding_dues, 0)

        self.assertEqual(self.member.dues_paid, expected_dues)


    def test_member_can_borrow_new_book(self):
        self.assertTrue(self.member.can_borrow_new_book)

        transaction = self.very_expensive_book.issue_to(self.member)

        self.assertTrue(self.member.can_borrow_new_book)

        transaction.update(borrowed_at=transaction.borrowed_at-datetime.timedelta(days=5))

        self.assertTrue(self.member.can_borrow_new_book)

        transaction.update(borrowed_at=transaction.borrowed_at-datetime.timedelta(days=6))

        self.assertFalse(self.member.can_borrow_new_book)


class TestMemberViews(MemberBaseTestCase):
    def test_list_members(self):
        url = url_for("members.list_members")

        response = self.client.get(url)

        self.assertIn(response.status_code, range(200, 400))

        self.assertIn(html.escape(self.member.name).encode(), response.data)
        self.assertIn(html.escape(self.member_2.name).encode(), response.data)

    def test_create_member_valid(self):
        url = url_for("members.create_member")

        response = self.client.post(url, data=self.valid_member_kwargs)

        self.assertIn(response.status_code, range(200, 400))

        self.assertIsNotNone(Member.query.filter_by(email=self.valid_member_kwargs["email"]).first())

    def test_create_member_invalid(self):
        url = url_for("members.create_member")

        response = self.client.post(url, data=self.invalid_member_kwargs)

        self.assertEqual(response.status_code, 400)

    def test_create_member_get(self):
        url = url_for("members.create_member")

        response = self.client.get(url)

        self.assertIn(response.status_code, range(200, 400))
