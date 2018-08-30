from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_html_and_a_title(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')

        self.assertTrue(html.startswith('<html>'))
        self.assertTrue(html.endswith('</html>'))

        self.assertIn('<title>Awesome To-Do Lists!</title>', html)
