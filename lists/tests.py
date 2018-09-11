from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_page_matches_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_displays_data_from_a_POST_request(self):
        response = self.client.post(
            '/', data={'new-todo-item': 'make breakfast'})

        self.assertIn('make breakfast', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_saves_items_only_if_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item')
        self.assertEqual(second_saved_item.text, 'The second item')

    def test_can_save_a_POST_request_to_db(self):
        response = self.client.post(
            '/', data={'new-todo-item': 'A new todo task'})

        self.assertEqual(Item.objects.count(), 1)
        newly_added_item = Item.objects.first()
        self.assertEqual(newly_added_item.text, 'A new todo task')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response['location'], '/')
