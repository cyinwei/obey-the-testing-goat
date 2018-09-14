from django.test import TestCase
from lists.models import Task


class HomePageTest(TestCase):
    def test_home_page_matches_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_saves_items_only_if_necessary(self):
        self.client.get('/')
        self.assertEqual(Task.objects.count(), 0)


class NewListTest(TestCase):
    def test_can_save_a_POST_request_to_db(self):
        self.client.post('/lists/new',
                         data={'new-todo-item': 'A new todo task'})

        self.assertEqual(Task.objects.count(), 1)
        newly_added_item = Task.objects.first()
        self.assertEqual(newly_added_item.text, 'A new todo task')

    def test_request_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'new-todo-item': 'The second todo task'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class TaskModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Task()
        first_item.text = 'The first (ever) item'
        first_item.save()

        second_item = Task()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Task.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item')
        self.assertEqual(second_saved_item.text, 'The second item')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        pass
        # todo_list = List.objects.create()
        # response = self.client.get(f'/lists/{todo_list.id}')
        # self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_tasks_for_that_list(self):
        Task.objects.create(text='make breakfast')
        Task.objects.create(text='learn TDD')

        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'make breakfast')
        self.assertContains(response, 'learn TDD')
