from datetime import date, datetime, timedelta

import pytest

from deps_high_sparrow.domain.model.document_type.validator.validation.exceptions import (
    CanNotOverrideName,
    CompareWithOptionalField,
    InvalidSyntax,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.business_validation.parser import (
    ValidationRuleParser as ValParser,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.frange import (
    frange,
)


def test_ValParser_get_variables():
    variables = {"a": 16, "b": 17}
    assert ValParser(variables=variables).variables == variables


@pytest.mark.parametrize(
    "function, expected_function",
    [
        ("min", min),
        ("max", max),
    ],
)
def test_ValParser__function_names(function, expected_function):
    parser = ValParser()
    assert parser._function_names[function] == expected_function

    assert parser._function_names["today"]
    assert parser._function_names["range"]
    assert parser._function_names["date"]


def test_ValParser_generic_visit_not_allowed():
    with pytest.raises(InvalidSyntax):
        ValParser().parse("import os")


def test_ValParser_invalid_syntax():
    with pytest.raises(InvalidSyntax) as exception:
        ValParser().parse("nothing to parse here")
        assert exception.msg == "Exactly one expression must be provided"


@pytest.mark.parametrize(
    "expression, result",
    [
        ("2 + 2 * 2", 6),
        ("2+2*2", 6),
        ("(2 + 2) * 2", 8),
        ("2 - 2 * 4", -6),
        ("(-2 - 2) * 4", -16),
        ("-2**2 * 4", -16),
        ("-2**2 * -4", 16),
        ("(-2)**2 * -4", -16),
        ("-2**(2 * 2)", -16),
        ("4**(1 / 2)", 2),
        ("2 / 2", 1),
        ("4 / 2 / 3", 2 / 3),
        ("-(-4) % 2", 0),
    ],
)
def test_ValParser_simple_expression(expression, result):
    assert ValParser().parse(expression) == result


@pytest.mark.parametrize(
    "custom_function, expression, result",
    [
        (lambda x: x + 1, "custom_function(3)", 4),
        (lambda x: x in range(0, 10), "custom_function(3)", True),
        (lambda x: x + 1 / 2 - x * 82, "custom_function(0)", 1 / 2),
        (lambda x: x + 1, "custom_function(3) + custom_function(0)", 5),
        (lambda x: x + 1, "custom_function(custom_function(0))", 2),
    ],
)
def test_ValParser_custom_function(custom_function, expression, result):
    parser = ValParser(functions={"custom_function": custom_function})
    actual_result = parser.parse(expression)
    assert actual_result == result


def test_ValParser_function_is_not_defined():
    with pytest.raises(InvalidSyntax):
        ValParser().parse("custom_function(9)")


@pytest.mark.parametrize(
    "field_value, expression, result",
    [
        (0, "FIELD == 0", True),
        (2, "FIELD * FIELD < 0", False),
        (-5, "FIELD - FIELD > -20", True),
        (0, "FIELD in range(1, 10)", False),
        ("my string", "FIELD == 'my string'", True),
        ("my string", "FIELD * 10", 10 * "my string"),
        (date(2020, 6, 29), "FIELD <= date(29, 7, 2020)", True),
    ],
)
def test_ValParser_field_value(field_value, expression, result):
    parser = ValParser(variables={"FIELD": field_value})
    actual_result = parser.parse(expression)
    assert actual_result == result


@pytest.mark.parametrize(
    "variables, expression, result",
    [
        ({"a": -1}, "+a", -1),
        ({"a": -1}, "-a", 1),
        ({"a": 17, "b": 18, "c": True}, "b - a - c", 0),
        (
            {"a": datetime(2020, 6, 29), "b": timedelta(days=365)},
            "a + b",
            datetime(2021, 6, 29),
        ),
        ({"a": "my string", "b": "my"}, "b in a", True),
    ],
)
def test_ValParser_set_variables(variables, expression, result):
    parser = ValParser(variables=variables)
    actual_result = parser.parse(expression)
    assert actual_result == result


def test_ValParser_division_by_zero():
    with pytest.raises(InvalidSyntax) as exception:
        ValParser(variables={"FIELD": 3}).parse("15* 18**7 / (3 - FIELD)")
        assert exception.msg


def test_ValParser_forbidden_variable():
    with pytest.raises(CanNotOverrideName) as exception:
        ValParser(variables={"a": 19, "None": 18}).parse("None + a")
        assert exception.msg == "Cannot override None"


def test_ValParser_optional_variable():
    with pytest.raises(CompareWithOptionalField):
        ValParser(variables={"a": 19}, optional_fields=["b"]).parse("a < b")


def test_ValParser_more_than_one_expression_provided():
    with pytest.raises(InvalidSyntax) as exception:
        ValParser(variables={"a": 19, "N": 18}).parse("N + 10; a+7")
        assert exception.msg


@pytest.mark.parametrize(
    "expression, result",
    [
        ("0 and 0", 0),
        ("0 or 5", 5),
        ("5 or 0", 5),
        ("True and False", False),
        ("False and True", False),
        ("False or True", True),
        ("True or False", True),
        ("False or False or True", True),
        ("(True and False) or (False or True)", True),
        ("True or 5/0", True),
        ("False and 5/0", False),
    ],
)
def test_ValParser_bool_op(expression, result):
    assert ValParser().parse(expression) == result


@pytest.mark.parametrize(
    "expression, result",
    [
        ("~1", -2),
        ("-4", -4),
        ("+4", +4),
        ("-(-4)", 4),
        ("not (not (-(+(-(~7)))))", True),
    ],
)
def test_ValParser_unary_op(expression, result):
    assert ValParser().parse(expression) == result


@pytest.mark.parametrize(
    "field_value, expression, result",
    [
        (2, "FIELD if FIELD < 3 else 0", 2),
        (2, "FIELD if FIELD > 3 else 0", 0),
        (2, "FIELD if FIELD > 3 else 0 if FIELD < 4 else 5", 0),
    ],
)
def test_ValParser_if_else(field_value, expression, result):
    parser = ValParser(variables={"FIELD": field_value})
    actual_result = parser.parse(expression)
    assert actual_result == result


@pytest.mark.parametrize(
    "expression, result",
    [
        ("2 >= 2", True),
        ("2 > 2", False),
        ("2 < 1", False),
        ("2 > 1", True),
        ("'my string 1' != 'my string 1'", False),
        ("'my string 1' == 'my string 2'", False),
        ("date(29, 7, 2020) == date(29, 7, 2020)", True),
    ],
)
def test_ValParser_comparison(expression, result):
    assert ValParser().parse(expression) == result


@pytest.mark.parametrize(
    "expression, result",
    [
        ("'bar' in 'foobar'", True),
        ("'baz' in 'foobar'", False),
        ("'foo' not in 'foobar'", False),
        ("'baz' not in 'foobar'", True),
    ],
)
def test_ValParser_in_not_in(expression, result):
    assert ValParser().parse(expression) == result


@pytest.mark.parametrize(
    "num, result",
    [
        ("2", 2),
        ("1-3j", 1 - 3j),
    ],
)
def test_ValParser_visit_num(num, result):
    assert ValParser().parse(num) == result


@pytest.mark.parametrize(
    "constant, result",
    [
        ("True", True),
        ("False", False),
        ("None", None),
    ],
)
def test_ValParser_visit_constant(constant, result):
    assert ValParser().parse(constant) == result


def test_ValParser_visit_internal_variable_name():
    assert ValParser().parse("True > False and False != None")


@pytest.mark.parametrize(
    "field, result",
    [
        ("a", False),
        ("b", False),
        ("c", True),
        ("d", False),
        ("f", True),
    ],
)
def test_ValParser_visit__is_optional(field, result):
    parser = ValParser(
        optional_fields=["a", "c", "f"],
        variables={"a": 1, "b": 2, "c": None, "d": None},
    )
    assert parser._is_optional(field) is result


@pytest.mark.parametrize(
    "name, expected_result",
    [
        ("True", True),
        ("False", False),
        ("None", None),
    ],
)
def test_ValParser_visit__variable_names(name, expected_result):
    parser = ValParser()
    assert parser._variable_names[name] is expected_result

    parser._variable_names = {"a": 10}
    actual_result = parser.parse("-a - 10")
    assert actual_result == -20

    actual_result = parser.parse("True")
    assert actual_result is True


@pytest.mark.parametrize(
    "expression, result",
    [
        ("3 in [1,2,3,4]", True),
        ("-3 in [1,2,3,4]", False),
        ("-3 not in [1,2,3,4]", True),
        ("3 in [1,2,3.0,4]", True),
        ("3.1 in [1,2,3,4]", False),
        ("3.1 not in [1,2,3,4]", True),
    ],
)
def test_ValParser_list(expression, result):
    assert ValParser().parse(expression) == result


@pytest.mark.parametrize(
    "expression, result",
    [
        ("3 in (1,2,3,4)", True),
        ("-3 in (1, 2, 3, 4)", False),
        ("-3 not in (1, 2, 3, 4)", True),
        ("3 in (1, 2, 3.0, 4)", True),
        ("3.1 in (1,2,3,4)", False),
        ("3.1 not in (1,2,3,4)", True),
    ],
)
def test_ValParser_tuple(expression, result):
    assert ValParser().parse(expression) == result


def test_ValParser__generator_with_one_iterable():
    assert list(ValParser().parse("(x for x in range(5))")) == list(frange(5))


def test_ValParser__list_comprehension_with_one_iterable():
    assert ValParser().parse("[x for x in range(5)]") == list(frange(5))


def test__ValParser__set_comprehension_with_one_iterable():
    assert ValParser().parse("{x for x in range(5)}") == set(frange(5))


def test_ValParser__list_comprehension_with_if_statement():
    assert ValParser().parse("[x for x in range(10) if x % 2]") == [x for x in frange(10) if x % 2]


def test_ValParser__list_comprehension_with_two_separate_variables():
    assert ValParser().parse("[x - y  for x in range(10) for y in range(5)]") == [
        x - y for x in frange(10) for y in frange(5)
    ]


def test_ValParser__list_comprehension_with_variables_as_tuple():
    assert ValParser().parse("[x-y+z for x,y,z in [(1,1,1),(2,2,2),(4,1,5)]]") == [
        x - y + z for x, y, z in [(1, 1, 1), (2, 2, 2), (4, 1, 5)]
    ]


def test_ValParser__list_comprehension_dependent_variables():
    assert ValParser().parse("[x*y+z for x in range(10) for y in range(x) for z in range(y)]") == [
        x * y + z for x in frange(10) for y in frange(x) for z in frange(y)
    ]


def test_ValParser__simple_dict_comprehension():
    assert ValParser().parse("{x**2:y**3 for x,y in [(1,2),(2,3),(3,4)]}") == {
        x**2: y**3 for x, y in [(1, 2), (2, 3), (3, 4)]
    }


def test_ValParser__dict_comprehension_separate_variables_with_conditions():
    assert ValParser().parse("{x ** 3: y - 7 for x in [9, 8, 7] for y in [4, 1, 2] if x % 2}") == {
        x**3: y - 7 for x in [9, 8, 7] for y in [4, 1, 2] if x % 2
    }


def test_ValParser__nested_comprehensions_different_iterable_name():
    assert ValParser().parse("[[x**3 for x in range(5)]for y in range(5)]") == [
        [x**3 for x in frange(5)] for _ in frange(5)
    ]


def test_ValParser__nested_comprehensions_same_iterable_name():
    assert ValParser().parse("[[x**3 for x in range(11) if x % 2 ] for x in range(19) if x % 2]") == [
        [x**3 for x in frange(11) if x % 2] for x in frange(19) if x % 2
    ]


def test_ValParser__indexing_list():
    assert ValParser().parse("[[1, 2, 3], {}][0]") == [1, 2, 3]
    assert ValParser().parse("[[1, 2, 3], {1}][1]") == {1}


def test_ValParser__int_float_functions():
    assert ValParser().parse("int('343')") == 343
    assert ValParser().parse("int(343.2)") == 343
    assert ValParser().parse("float('343.2')") == 343.2
