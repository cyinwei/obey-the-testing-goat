import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAITS = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def _check_for_task_in_todo_list(self, task_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id-todo-list')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(task_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAITS:
                    raise e
                time.sleep(0.5)

    def _submit_todo_task(self, task_text):
        # re-get the inputbox, since the page might have refreshed
        inputbox = self.browser.find_element_by_id('id-new-todo-item-input')
        inputbox.send_keys(task_text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kobe has a heard of the awesome ToDo app, superlists.  He visits
        # the homepage.
        self.browser.get(self.live_server_url)

        # He looks as the title and confirms he's on the right URL
        self.assertIn('Awesome To-Do List', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Awesome To-Do List', header_text)

        # Kobe sees an invitation to enter a ToDo task
        inputbox = self.browser.find_element_by_id('id-new-todo-item-input')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter the vision you wish to bring to reality')

        # He types "Become governor of California" into a text box as a task
        # and submits it by pressing ENTER
        self._submit_todo_task('Become governor of California')

        # After submitting, he sees an updated ToDo list that looks like
        # "1: Become governor of California" as an item in a to-do list
        self._check_for_task_in_todo_list('1. Become governor of California')

        # Kobe then enters "Become president of the United States", as that is
        # his next task.
        self._submit_todo_task('Become president of the United States')

        # He sees the new entry on the ToDo list after the page refreshes
        self._check_for_task_in_todo_list(
            '2. Become president of the United States')

        # Satisfied, he starts implementing his ToDo list
        return

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Lebron starts a new ToDo list
        self.browser.get(self.live_server_url)

        # He adds a task, 'Get an Oscar'
        self._submit_todo_task('Get an Oscar')
        self._check_for_task_in_todo_list('1. Get an Oscar')

        # He notices that his list has an unique URL
        lebron_list_url = self.browser.current_url
        self.assertRegex(lebron_list_url, '/lists/.+')

        # A new user, Curry goes to the web app

        # # We use a new browser session to make sure that no information
        # # of Lebron's is coming through from cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Curry visits the home page; there's no sign of Lebron's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Get an Oscar', page_text)

        # Curry then enters a task, 'Make UA the next Nike'
        self._submit_todo_task('Make UA the next Nike')
        self._check_for_task_in_todo_list('1. Make UA the next Nike')

        # Curry's ToDo list gets its own URL
        curry_list_url = self.browser.current_url
        self.assertRegex(curry_list_url, '/lists/.+')
        self.assertNotEqual(lebron_list_url, curry_list_url)

        # Curry makes sure there's no trace of Lebron's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Get an Oscar', page_text)
        self.assertIn('Make UA the next Nike', page_text)

        # Satisfied, both MVPs do MVP things
        return

    def test_layout_and_styling(self):
        # Donavan Mitchell goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the ToDo input box is nicely centered
        inputbox = self.browser.find_element_by_id('id-new-todo-item-input')
        self.assertAlmostEqual(inputbox.location['x']
                               + inputbox.size['width'] / 2,
                               512,
                               delta=10)
