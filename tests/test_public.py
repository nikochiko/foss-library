from flask import url_for

from .base import BaseTest


class TestPublicViews(BaseTest):
    def test_home(self):
        response = self.client.get(url_for("public.home"))

        self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.client.get("/notexistentlink")

        self.assertEqual(response.status_code, 404)
