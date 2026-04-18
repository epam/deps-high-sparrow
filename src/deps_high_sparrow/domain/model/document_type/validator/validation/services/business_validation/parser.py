import ast
import logging
import operator
import re
from datetime import date
from typing import List

from ...exceptions import (
    CanNotOverrideName,
    CompareWithOptionalField,
    InvalidSyntax,
    NameIsNotDefined,
)
from ..frange import frange
from ..utils import has_value
from .predefined_functions import (
    check_dependency,
    compare_dates,
    find_value_by_key,
    get_table_cell,
    is_city,
    is_postal_code,
    is_state,
    is_telephone,
    is_unique,
    merge_whitespaces,
    regex_match,
    str_replace_endings,
    to_date,
    today,
    validate_country_code,
    validate_currency_code,
    validate_date_for_specific_format,
    validate_field_content,
    validate_phone_number,
    validate_phone_number_for_country,
    validate_ssn_content,
    validate_ssn_format,
    validate_timedelta,
)

logger = logging.getLogger(__name__)


class ValidationRuleParser(ast.NodeVisitor):
    _boolean_ops = {ast.And: operator.and_, ast.Or: operator.or_}

    _binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _unary_ops = {
        ast.Invert: operator.inv,
        ast.Not: operator.not_,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    _compare_ops = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
        ast.In: lambda x, y: x in y,
        ast.NotIn: lambda x, y: x not in y,
    }

    _variable_names = {"True": True, "False": False, "None": None}

    # Predefined functions
    _function_names = {
        "cell": get_table_cell,
        "all": all,
        "any": any,
        "len": len,
        "min": min,
        "max": max,
        "int": int,
        "bool": bool,
        "float": float,
        "today": lambda: date.today(),
        "range": frange,
        "date": to_date,
        "lower": lambda x: x.lower(),
        "is_currency_code": validate_currency_code,
        "is_country_code": validate_country_code,
        "is_phone_number": validate_phone_number,
        "is_phone_number_for_country": validate_phone_number_for_country,
        "is_unique": is_unique,
        "is_alpha": lambda x: x.isalpha(),
        "is_name": lambda x: bool(re.compile("[a-zA-Z ']*").fullmatch(x)),
        "is_numeric": lambda x: bool(re.compile("[0-9()+ ]*").fullmatch(x)),
        "is_state": is_state,
        "is_postal_code": is_postal_code,
        "is_city": is_city,
        "is_telephone": is_telephone,
        "check_dependency": check_dependency,
        "validate_ssn_format": validate_ssn_format,
        "validate_ssn_content": validate_ssn_content,
        "validate_date_for_specific_format": validate_date_for_specific_format,
        "validate_field_content": validate_field_content,
        "regex_match": regex_match,
        "validate_timedelta": validate_timedelta,
        "compare_dates": compare_dates,
        "today_iso": today,
        "str_replace_endings": str_replace_endings,
        "merge_whitespaces": merge_whitespaces,
        "find_value_by_key": find_value_by_key,
    }

    def __init__(self, variables=None, functions=None, optional_fields=None):
        self._variables = None
        self.variables = variables

        self._functions = functions or {}
        self._optional_fields = optional_fields or []

        self._used_variables = set()

    def parse(self, expression):
        """Parse a string `expression` and return its result."""
        try:
            return self.visit(ast.parse(expression))
        except CompareWithOptionalField as e:
            logger.error(e, exc_info=True)
            raise
        except Exception as exception:
            logger.error(exception, exc_info=True)
            raise InvalidSyntax(exception.args[0])

    @property
    def variables(self):
        return self._variables.copy()

    @variables.setter
    def variables(self, variables):
        """Set a new variable scope for the expression parser."""

        if variables is None:
            variables = {}
        else:
            variables = variables.copy()

        variable_names = set(variables.keys())
        constant_names = set(self._variable_names.keys())
        forbidden_variables = variable_names.intersection(constant_names)
        if forbidden_variables:
            raise CanNotOverrideName(forbidden_variables)

        self._variables = variables

    @property
    def used_variables(self):
        return self._used_variables.copy()

    @used_variables.deleter
    def used_variables(self):
        self._used_variables.clear()

    def update_variable(self, variable):
        variable_name = list(variable)[0]
        if variable_name not in self._variable_names.keys():
            self._variables[variable_name] = variable[variable_name]
            return
        raise CanNotOverrideName(variable)

    def generic_visit(self, node):
        """
        Visitor for nodes that do not have a custom visitor.
        This visitor denies any nodes that may not be part of the expression.
        """

        raise InvalidSyntax(f"Node {ast.dump(node)} not allowed")

    def visit_Module(self, node):
        """Visit the root module node."""

        if len(node.body) != 1:
            raise InvalidSyntax("Exactly one expression must be provided")

        return self.visit(node.body[0])

    def visit_Expr(self, node):
        """Visit an expression node."""

        return self.visit(node.value)

    def visit_BoolOp(self, node):
        """Visit a boolean expression node."""

        if isinstance(node.op, ast.And):
            result = self.visit(node.values[0])
            for value in node.values[1:]:
                if not result:
                    return result
                result = self.visit(value)
            return result

        elif isinstance(node.op, ast.Or):
            result = self.visit(node.values[0])
            for value in node.values[1:]:
                if result:
                    return result
                result = self.visit(value)
            return result

    def visit_BinOp(self, node):
        """Visit a binary expression node."""

        op = type(node.op)
        func = self._binary_ops[op]
        return func(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        """Visit a unary expression node."""

        op = type(node.op)
        func = self._unary_ops[op]
        return func(self.visit(node.operand))

    def visit_IfExp(self, node):
        """Visit an inline if..else expression node."""

        return self.visit(node.body) if self.visit(node.test) else self.visit(node.orelse)

    def visit_Compare(self, node):
        """Visit a comparison expression node."""

        result = self.visit(node.left)
        for local_operator, comparator in zip(node.ops, node.comparators):
            op = type(local_operator)
            func = self._compare_ops[op]
            result = func(result, self.visit(comparator))

        return result

    def visit_Call(self, node):
        """Visit a function call node."""

        name = node.func.id
        if name in self._functions:
            func = self._functions[name]
        elif name in self._function_names:
            func = self._function_names[name]
        else:
            raise NameIsNotDefined(name)

        args = [self.visit(arg) for arg in node.args]
        keywords = dict([self.visit(keyword) for keyword in node.keywords])
        return func(*args, **keywords)

    def visit_Constant(self, node):
        return node.n

    def visit_Name(self, node):
        """Visit a named variable node."""

        if self._is_optional(node.id):
            logger.info(f"Optional field {node.id} without value")
            raise CompareWithOptionalField(node.id)

        elif node.id in self._variables:
            self._used_variables.add(node.id)
            return self._variables[node.id]

        elif node.id in self._variable_names:
            return self._variable_names[node.id]

        raise NameIsNotDefined(node.id)

    def visit_List(self, node):
        return [self.visit(item) for item in node.elts]

    def visit_Tuple(self, node):
        tuple_items = node.elts
        return tuple(self.visit(item) for item in tuple_items)

    def visit_GeneratorExp(self, node):
        return self._recursive_for(node.generators, node.elt)

    def visit_ListComp(self, node: ast.ListComp) -> List:
        return list(self._recursive_for(node.generators, node.elt))

    def visit_SetComp(self, node: ast.SetComp) -> set:
        return set(self._recursive_for(node.generators, node.elt))

    def visit_DictComp(self, node: ast.DictComp) -> dict:
        return dict(self._recursive_for(node.generators, ast.Tuple(elts=[node.key, node.value], ctx=ast.Load())))

    def visit_Subscript(self, node: ast.Subscript):
        value = self.visit(node.value)
        index = self.visit(node.slice)

        return value[index]

    def visit_Dict(self, node):
        return {self.visit(k): self.visit(v) for k, v in zip(node.keys, node.values)}

    def visit_Set(self, node):
        return {self.visit(e) for e in node.elts}

    def _is_optional(self, field):
        if field in self._optional_fields:
            return (field not in self._variables) or (not has_value(self._variables[field]))
        return False

    def _recursive_for(self, cycles: List[ast.comprehension], function):
        cycles_copy = cycles.copy()

        next_cycle = cycles_copy.pop(0)
        # if comprehension is like (f(x,y) for x,y in A) then x, y is a tuple.
        iterable = (
            tuple(name.id for name in next_cycle.target.elts)  # type: ignore
            if isinstance(next_cycle.target, ast.Tuple)
            else next_cycle.target.id  # type: ignore
        )

        iterator = self.visit(next_cycle.iter)

        for temp_var in iterator:
            (local_temp_var, local_iterable) = (
                (temp_var, iterable) if isinstance(iterable, tuple) else ((temp_var,), (iterable,))
            )
            for index, keyname in enumerate(local_iterable):
                self.update_variable({keyname: local_temp_var[index]})
            ifs = all((self.visit(statement) for statement in next_cycle.ifs))
            if not ifs:
                continue
            elif cycles_copy:
                yield from self._recursive_for(cycles_copy, function)
                continue
            yield self.visit(function)
