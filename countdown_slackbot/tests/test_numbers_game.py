import unittest


from countdown_slackbot import numbers


class TestNumbers(unittest.TestCase):

    def test_random_pop(self):
        some_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for i in range(5):
            original_length = len(some_list)
            popped_item = numbers.random_pop(some_list)
            self.assertNotIn(popped_item, some_list)
            self.assertEqual(len(some_list), original_length - 1)

    def test_basic_number_rows(self):
        top_row, bottom_row = numbers.get_basic_number_rows()

        self.assertEqual(
            top_row,
            [25, 50, 75, 100]
        )

        self.assertEqual(
            bottom_row,
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
        )

    def test_non_int_pick_numbers(self):
        """An integer must be given to pick_numbers.
        """
        for bad_arg in [None, "1", 1.0, "foo", [1]]:
            with self.assertRaises(ValueError):
                numbers.pick_numbers(bad_arg)

    def test_out_of_range_numbers(self):
        """We can only allow 0..4 (inclusive) numbers from the top.
        """
        for i in [0, 1, 2, 3, 4]:
            # this will work!
            numbers.pick_numbers(i)

        # These won't
        for bad_arg in [-1, 5, 6, 7]:
            with self.assertRaises(ValueError):
                numbers.pick_numbers(bad_arg)

    def test_not_enough_numbers(self):
        """We can't request more numbers than exist in the rows.
        """
        # This is fine...
        numbers.pick_numbers(num_from_top_row=4, total_num_required=10)

        # This is not...
        with self.assertRaises(ValueError):
            numbers.pick_numbers(num_from_top_row=4, total_num_required=25)
