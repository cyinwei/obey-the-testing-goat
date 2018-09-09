from django.test import TestCase


class HomePageTest(TestCase):
    def test_home_page_matches_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_saves_a_POST_request(self):
        response = self.client.post(
            '/', data={'new-todo-item-text': 'make breakfast'})

        self.assertIn('make breakfast', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'lists/home.html')
