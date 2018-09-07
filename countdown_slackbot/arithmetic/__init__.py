from contextlib import contextmanager
from copy import deepcopy

from .parsing import raw_parse


class AvailableNumbers():

    def __init__(self, numbers=None):
        self._numbers = None
        self.numbers = numbers

    def __contains__(self, number):
        return number in self.numbers

    @contextmanager
    def do_in_transaction(self):
        temp = AvailableNumbers(deepcopy(self.numbers))
        try:
            yield temp
        except:
            raise
        else:
            # No exception! That's good.
            self.numbers = temp.numbers

    @property
    def numbers(self):
        return self._numbers

    @numbers.setter
    def numbers(self, numbers):
        self._numbers = numbers if numbers else []

    def remove(self, number):
        try:
            self.numbers.remove(number)
        except ValueError:
            raise UnavailableNumberError(number)

    def add(self, number):
        self.numbers.append(number)


class InfiniteNumbers():

    def __init__(self):
        pass

    def __contains__(self, number):
        return True

    @contextmanager
    def do_in_transaction(self):
        yield self

    @property
    def numbers(self):
        return None

    @numbers.setter
    def numbers(self, numbers):
        pass

    def set_numbers(self, numbers):
        pass

    def remove(self, number):
        pass

    def add(self, number):
        pass


class ExpressionTerm():
    def __init__(self, term):
        self.term = term

    def evaluate(self, available_numbers):
        with available_numbers.do_in_transaction() as nums:
            nums.remove(self.term)
            return self.term

    def __repr__(self):
        return "ExpressionTerm({})".format(self.term)

    def __str__(self):
        return "{}".format(self.term)


class ExpressionBinOp():
    def __init__(self, term_1, op, term_2):
        self.term_1 = term_1
        self.op = op
        self.term_2 = term_2

    def evaluate(self, available_numbers):
        with available_numbers.do_in_transaction() as nums:
            result_1 = self.term_1.evaluate(nums)
            result_2 = self.term_2.evaluate(nums)
            if self.op == "+":
                final_result = result_1 + result_2
            elif self.op == "-":
                final_result = result_1 - result_2
            elif self.op == "*":
                final_result = result_1 * result_2
            elif self.op == "/":
                quotient, remainder = divmod(result_1, result_2)
                if remainder != 0:
                    raise NonIntDivisionError()
                final_result = quotient
            else:
                raise InvalidOperatorError(self.op)

            nums.add(final_result)
            return final_result

    def __repr__(self):
        return "ExpressionBinOp({}, {}, {})".format(self.term_1, self.op, self.term_2)

    def __str__(self):
        return "({} {} {})".format(str(self.term_1), self.op, str(self.term_2))


class Assertion():
    def __init__(self, primary_expression, other_expressions):
        self.primary_expression = primary_expression
        self.other_expressions = other_expressions

    def evaluate(self, available_numbers):

        primary_result = self.primary_expression.evaluate(available_numbers)

        for expr in self.other_expressions:
            result = expr.evaluate(InfiniteNumbers())
            if result != primary_result:
                raise InvalidAssertionError("{} != {}".format(self.primary_expression, expr))

        return primary_result

    def __repr__(self):
        return "Assertion({}, [{}])".format(
            self.primary_expression,
            ", ".join("{}".format(expr) for expr in self.other_expressions),
        )

    def __str__(self):
        all_expressions = [self.primary_expression] + self.other_expressions
        strings = [str(expr) for expr in all_expressions]
        return " = ".join(strings)


def parse(s):
    result = raw_parse(s)
    if result[0] == "assertion":
        return Assertion(
            _to_expression(result[1]),
            [_to_expression(other) for other in result[2]],
        )
    elif result[0] == "expression":
        return Assertion(_to_expression(result[1]), [])


def _to_expression(raw_expression):
    if isinstance(raw_expression, tuple):
        return ExpressionBinOp(
            _to_expression(raw_expression[0]),
            raw_expression[1],
            _to_expression(raw_expression[2]),
        )
    else:
        return ExpressionTerm(raw_expression)


class UnavailableNumberError(Exception):
    pass


class NonIntDivisionError(Exception):
    pass


class InvalidOperatorError(Exception):
    pass


class InvalidAssertionError(Exception):
    pass
