from django.test import TestCase
from lists.models import Task, List


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


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        learn_list = List.objects.create()

        self.client.post(f'/lists/{learn_list.id}/add_task',
                         data={'new-todo-item': 'Learn Elm'})

        self.assertEqual(Task.objects.count(), 1)
        new_task = Task.objects.first()
        self.assertEqual(new_task.text, 'Learn Elm')
        self.assertEqual(new_task.parent_list, learn_list)

    def test_redirects_to_list_view(self):
        learn_list = List.objects.create()

        response = self.client.post(f'/lists/{learn_list.id}/add_task',
                                    data={'new-todo-item': 'Learn Elm'})

        self.assertRedirects(response, f'/lists/{learn_list.id}/')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        todo_list = List.objects.create()
        response = self.client.get(f'/lists/{todo_list.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_tasks_for_that_list(self):
        chore_list = List.objects.create()
        Task.objects.create(text='make breakfast', parent_list=chore_list)
        Task.objects.create(text='wash dishes', parent_list=chore_list)

        learn_list = List.objects.create()
        Task.objects.create(text='do ch. 7 of obey the testing goat',
                            parent_list=learn_list)
        Task.objects.create(text='do ch. 8 of obey the testing goat',
                            parent_list=learn_list)

        chore_page_response = self.client.get(f'/lists/{chore_list.id}/')
        self.assertContains(chore_page_response, 'make breakfast')
        self.assertContains(chore_page_response, 'wash dishes')
        self.assertNotContains(chore_page_response,
                               'do ch. 7 of obey the testing goat')
        self.assertNotContains(chore_page_response,
                               'do ch. 8 of obey the testing goat')

    def test_passes_correct_list_to_template(self):
        chore_list = List.objects.create()
        learn_list = List.objects.create()
        response = self.client.get(f'/lists/{learn_list.id}/')
        self.assertNotEqual(response.context['parent_list'], chore_list)
        self.assertEqual(response.context['parent_list'], learn_list)


class ListAndTaskModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_list = List()
        first_list.save()

        first_item = Task()
        first_item.text = 'The first (ever) item'
        first_item.parent_list = first_list
        first_item.save()

        second_item = Task()
        second_item.text = 'The second item'
        second_item.parent_list = first_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, first_list)

        saved_items = Task.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item')
        self.assertEqual(second_saved_item.text, 'The second item')
        self.assertEqual(first_saved_item.parent_list, first_list)
        self.assertEqual(second_saved_item.parent_list, first_list)

