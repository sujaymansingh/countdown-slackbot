import unittest


import countdown_slackbot


class TestNumbers(unittest.TestCase):

    def test_random_pop(self):
        some_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for i in range(5):
            original_length = len(some_list)
            popped_item = countdown_slackbot.random_pop(some_list)
            self.assertNotIn(popped_item, some_list)
            self.assertEqual(len(some_list), original_length - 1)
