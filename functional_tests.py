from selenium import webdriver
import unittest

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
        assert 'Awesome To-Do Lists' in self.browser.title

        # Kobe sees an invitation to enter a ToDo task
        self.fail('Finish the functional tests!')

        # He types "become governor of California" into a text box as a task

        # After submitting, he sees an updated ToDo list that looks like
        # "1: Become governor of California" as an item in a to-do list

        # There's a still input following the item.  Kobe then enters
        # "Become president of the United States"

        # Kobe wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.

        # Kobe checks that url just to be safe.  His ToDo list is still there.

        # Satisfied, he starts implementing his ToDo list

if __name__ == '__main__':
    unittest.main()
