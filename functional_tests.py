import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kobe has a heard of the awesome ToDo app, superlists.  He visits
        # the homepage.
        self.browser.get('http://localhost:8000')

        # He looks as the title and confirms he's on the right URL
        self.assertIn('Awesome To-Do Lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Awesome To-Do Lists', header_text)

        # Kobe sees an invitation to enter a ToDo task
        inputbox = self.browser.find_element_by_id('id-new-todo-item-input')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter the vision you wish to bring to reality')
        # He types "Become governor of California" into a text box as a task
        inputbox.send_keys('Become governor of California')

        # He submits the task
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # After submitting, he sees an updated ToDo list that looks like
        # "1: Become governor of California" as an item in a to-do list
        table = self.browser.find_element_by_id('id-todo-list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            '1. Become governor of California', [row.text for row in rows],
            (f"New to-do item did not appear in table.  "
             f"List contents were: \n{table.text}")
        )

        # Kobe then enters "Become president of the United States", as that is
        # his next task.

        # get the inputbox after the site is refreshed
        inputbox = self.browser.find_element_by_id('id-new-todo-item-input')
        inputbox.send_keys('Become president of the United States')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # He sees the new entry on the ToDo list after the page refreshes

        # get the table again after the site is refreshed
        table = self.browser.find_element_by_id('id-todo-list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            '2. Become president of the United States',
            [row.text for row in rows],
            (f'Second to-do item did not appear in table.  '
             f'List contents were: \n{table.text}')
        )

        self.fail('Finish the functional tests!')

        # Kobe wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.

        # Kobe checks that url just to be safe.  His ToDo list is still there.

        # Satisfied, he starts implementing his ToDo list


if __name__ == '__main__':
    unittest.main()
