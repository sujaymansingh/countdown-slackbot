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


class TestOperator(unittest.TestCase):

    def test_call(self):
        self.assertEqual(numbers.PLUS(18, 6), 24)
        self.assertEqual(numbers.SUBTRACT(18, 6), 12)
        self.assertEqual(numbers.MULTIPLY(18, 6), 108)
        self.assertEqual(numbers.DIVIDE(18, 6), 3)


class TestCalculation(unittest.TestCase):

    def test_simple_parse(self):
        line = "45 / 3 = 15"
        result = numbers.Calculation.parse(line)

        self.assertEqual(result.num_1, 45)
        self.assertEqual(result.operator, numbers.DIVIDE)
        self.assertEqual(result.num_2, 3)
        self.assertEqual(result.asserted_result, 15)

    def test_apply(self):
        nums = [1, 2, 4, 8]

        with self.assertRaises(numbers.NumberNotPresentError):
            doesnt_have_5 = numbers.Calculation(num_1=5, num_2=4, operator=numbers.PLUS, asserted_result=9)
            doesnt_have_5.apply(nums)

        with self.assertRaises(numbers.InvalidAssertionError):
            bad_assertion = numbers.Calculation(num_1=1, num_2=2, operator=numbers.SUBTRACT, asserted_result=100)
            bad_assertion.apply(nums)

        good_calculation = numbers.Calculation(num_1=8, num_2=4, operator=numbers.DIVIDE, asserted_result=2)
        good_calculation.apply(nums)

        self.assertNotIn(4, nums)
        self.assertNotIn(8, nums)

        self.assertCountEqual(nums, [1, 2, 2])
