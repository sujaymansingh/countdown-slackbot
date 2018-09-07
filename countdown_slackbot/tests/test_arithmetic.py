from unittest import TestCase

from ..arithmetic import AvailableNumbers, InfiniteNumbers, ExpressionBinOp, ExpressionTerm, UnavailableNumberError
from ..arithmetic.parsing import raw_parse


class TestAvailableNumbers(TestCase):

    def test_removing_and_adding(self):
        n = AvailableNumbers()

        n.numbers = [1, 2, 3]

        n.add(4)
        self.assertEqual(n.numbers, [1, 2, 3, 4])

        n.remove(3)
        n.remove(1)
        self.assertEqual(n.numbers, [2, 4])

        with self.assertRaises(UnavailableNumberError):
            n.remove(42)

    def test_transaction_fail(self):
        n = AvailableNumbers([1, 2, 3])

        with self.assertRaises(UnavailableNumberError):
            with n.do_in_transaction() as nums:
                nums.remove(1)
                nums.remove(2)

                # The following will fail!
                nums.remove(42)

        # but, n should be unaffected.
        self.assertIn(1, n)
        self.assertIn(2, n)
        self.assertIn(3, n)

    def test_transaction_succeed(self):
        n = AvailableNumbers([1, 2, 3])

        with n.do_in_transaction() as nums:
            nums.remove(1)
            nums.remove(2)

        self.assertNotIn(1, n)
        self.assertNotIn(2, n)
        self.assertIn(3, n)


class TestExpression(TestCase):

    def test_simple_expression(self):
        exp = ExpressionBinOp(ExpressionTerm(6), "+", ExpressionTerm(9))
        result = exp.evaluate(InfiniteNumbers())
        self.assertEqual(result, 15)

    def test_complex_expression(self):
        expression = ExpressionBinOp(
            ExpressionBinOp(ExpressionTerm(9), "+", ExpressionTerm(15)),
            "*",
            ExpressionBinOp(ExpressionTerm(10), "-", ExpressionTerm(6)),
        )
        result = expression.evaluate(InfiniteNumbers())
        self.assertEqual(result, 96)

    def test_with_available_numbers(self):
        expression = ExpressionBinOp(
            ExpressionBinOp(ExpressionTerm(9), "+", ExpressionTerm(15)),
            "/",
            ExpressionTerm(6),
        )
        available_numbers = AvailableNumbers([9, 15, 6, 25])
        result = expression.evaluate(available_numbers)

        self.assertEqual(result, 4)
        self.assertIn(25, available_numbers)
        self.assertIn(24, available_numbers)

    def test_with_missing_number(self):
        expression = ExpressionBinOp(
            ExpressionBinOp(ExpressionTerm(9), "+", ExpressionTerm(15)),
            "/",
            ExpressionTerm(6),
        )
        available_numbers = AvailableNumbers([9, 15, 25])

        with self.assertRaises(UnavailableNumberError):
            expression.evaluate(available_numbers)

        # The 9 and the 15 should still remain
        self.assertIn(9, available_numbers)
        self.assertIn(15, available_numbers)
        self.assertIn(25, available_numbers)

    #    def test_assertion_no_available_numbers(self):
    #        assertion = (
    #            "assertion",
    #            (7, "*", (6, "+", 4)),
    #            [(7, "*", 10), 70],
    #        )
    #        self.assertTrue(evaluate(assertion, None))

    # from ..arithmetic import evaluate
    #
    #


class TestRawParse(TestCase):

    def test_simple_expression(self):
        result = raw_parse("6 + 4")
        self.assertEqual(result, ("expression", (6, "+", 4)))

    def test_complex_expression(self):
        result = raw_parse("(6 + 4) * 7")
        self.assertEqual(
            result,
            (
                "expression",
                ((6, "+", 4), "*", 7),
            ),
        )

    def test_assertion(self):
        result = raw_parse("7 * (6 + 4) = 70")
        self.assertEqual(
            result,
            (
                "assertion",
                (7, "*", (6, "+", 4)),
                [70],
            ),
        )

    def test_multiple_assertions(self):
        result = raw_parse("7 * (6 + 4) = 7* 10 = 70")
        self.assertEqual(
            result,
            (
                "assertion",
                (7, "*", (6, "+", 4)),
                [(7, "*", 10), 70],
            ),
        )
    #
    #
    # class TestEvaluate(TestCase):
    #
    #    def test_assertion_no_available_numbers(self):
    #        assertion = (
    #            "assertion",
    #            (7, "*", (6, "+", 4)),
    #            [(7, "*", 10), 70],
    #        )
    #        self.assertTrue(evaluate(assertion, None))
