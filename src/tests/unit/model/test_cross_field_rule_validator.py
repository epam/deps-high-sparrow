import pytest

from deps_high_sparrow.domain.exceptions import RuleFieldReferencesMismatchError


@pytest.mark.parametrize(
    "rule,validated_fields,dependent_fields",
    [
        ("Funknown > 0", ["field1"], []),
        ("type_code__unknown > 0", ["field1"], []),
        ("Fitem_of__unknown != 0", ["field1"], []),
        ("Fitem_of__unknown__0 == 'key'", ["field1"], []),
        ("Fitem_of__unknown__1 == 'val'", ["field1"], []),
        ("Funknown__0 == 'key'", ["field1"], []),
        ("Funknown__0 > Funknown__1", ["field1"], []),
        ("Ffield1 > 0 and Funknown > 0", ["field1"], []),
        ("Ffield1 > Funknown", ["field1"], ["field2"]),
        ("len(Funknown) > 5", ["field1"], []),
        ("Funknown[0] > 100", ["field1"], []),
        ("min(Ffield1, Funknown) > 0", ["field1"], []),
        ("Funknown[0][0] == 'v'", ["field1"], []),
        ("Funknown[1][0] == 'k'", ["field1"], []),
        ("check_dependency(Funknown__0, Funknown__1)", ["field1"], []),
        ("check_dependency(type_code__unknown__0, type_code__unknown__1)", ["field1"], []),
        ("Funknown > 0", [], ["dep_field"]),
        ("type_code__unknown > 0", [], ["dep_field"]),
        ("len(Fagg_unknown_field) > 0", ["agg_claim_table"], []),
        ("Fagg_unknown_field[0] > 100", ["agg_claim_table"], []),
        ("len(Fitem_of__agg_unknown_field) > 0", ["agg_claim_table"], []),
        ("Fitem_of__agg_unknown_field__0 == Fagg_claim_table", ["agg_claim_table"], []),
        ("int(cell(Fagg_unknown_field, 0, 0)) == 1", ["agg_claim_table"], []),
        ("(int(Fagg_unknown_field__0) + int(Fagg_unknown_field__1)) > 10", ["agg_claim_table"], []),
        ("all(x > 0 for x in Fagg_unknown_field)", ["agg_claim_table"], []),
        ("compare_dates(Fagg_claim_table, Fagg_unknown_field) < 0", ["agg_claim_table"], []),
        ("Fagg_claim_table > 0 and len(Fagg_unknown_field) > 0", ["agg_claim_table"], []),
        ("len(type_code__agg_unknown_field) > 5", ["agg_claim_table"], []),
        ("type_code__agg_unknown_field[0] > 100", ["agg_claim_table"], []),
        ("min(type_code__agg_claim_table, type_code__agg_unknown_field) > 0", ["agg_claim_table"], []),
        ("len(type_code__item_of__agg_unknown_field) > 0", ["agg_claim_table"], []),
        ("type_code__item_of__agg_unknown_field__0 == type_code__agg_claim_table", ["agg_claim_table"], []),
        ("int(cell(type_code__agg_unknown_field, 0, 0)) == 1", ["agg_claim_table"], []),
        ("all(x > 0 for x in type_code__agg_unknown_field)", ["agg_claim_table"], []),
        ("compare_dates(type_code__agg_claim_table, type_code__agg_unknown_field) < 0", ["agg_claim_table"], []),
        ("Fagg_unknown_field[0][0] == 'v'", ["agg_claim_table"], []),
        ("check_dependency(Fagg_unknown_field__0, Fagg_unknown_field__1)", ["agg_claim_table"], []),
        ("check_dependency(type_code__agg_unknown_field__0, type_code__agg_unknown_field__1)", ["agg_claim_table"], []),
        ("len(Fagg_unknown_field) > 5", [], ["dep_claim_ref"]),
        ("Fagg_unknown_field[0][0] == 'v'", [], ["dep_claim_ref"]),
        ("Fagg_claim_table > 0 and Fagg_unknown_field > 0", ["agg_claim_table"], ["dep_claim_ref"]),
    ],
)
def test_validate__rule_references_unknown_field__raises(
    rule_field_references_validator,
    rule,
    validated_fields,
    dependent_fields,
):
    with pytest.raises(RuleFieldReferencesMismatchError):
        rule_field_references_validator.validate(
            rule=rule,
            validated_fields=validated_fields,
            dependent_fields=dependent_fields,
        )


@pytest.mark.parametrize(
    "rule,validated_fields,dependent_fields",
    [
        ("Ffield1 > 0", ["field1", "field2"], []),
        ("type_code__field1 > 0", ["field1", "field2"], []),
        ("Fitem_of__field1 != 0", ["field1", "field2"], []),
        ("Fitem_of__field1__0 == 'key'", ["field1", "field2"], []),
        ("Fitem_of__field1__1 == 'val'", ["field1", "field2"], []),
        ("Ffield1__0 == 'key'", ["field1", "field2"], []),
        ("Ffield1 > 0", ["field1"], ["dep_field"]),
        ("type_code__field1 > 0", ["field1"], ["dep_field"]),
        ("Fdep_field > 0", ["field1"], ["dep_field"]),
        ("Ffield1 > Fdep_field", ["field1", "extra"], ["dep_field"]),
        ("len(Ffield1) > 0", ["field1", "field2"], []),
        ("Ffield1[0] == 1", ["field1", "field2"], []),
        ("min(Ffield1, 0) > -1", ["field1", "field2"], []),
        ("int(cell(Ffield1, 0, 0)) == 1", ["field1", "field2"], []),
        ("(int(Ffield1__0) + 1) > 0", ["field1", "field2"], []),
        ("all(x > 0 for x in Ffield1)", ["field1", "field2"], []),
        ("Ffield1[0][0] == 'v'", ["field1", "field2"], []),
        ("check_dependency(Ffield1__0, Ffield1__1)", ["field1", "field2"], []),
        ("check_dependency(type_code__field1__0, type_code__field1__1)", ["field1", "field2"], []),
        ("int(cell(Ffield1, 0, 0)) == 1", ["field1"], ["dep_field"]),
        ("int(cell(type_code__field1, 0, 0)) == 1", ["field1"], ["dep_field"]),
        ("Fagg_claim_table > 0", ["agg_claim_table", "claim_amount"], []),
        ("type_code__agg_claim_table > 0", ["agg_claim_table", "claim_amount"], []),
        ("Fitem_of__agg_claim_table != 0", ["agg_claim_table", "claim_amount"], []),
        ("Fitem_of__agg_claim_table__0 == 'key'", ["agg_claim_table", "claim_amount"], []),
        ("len(Fagg_claim_table) > 0", ["agg_claim_table", "claim_amount"], []),
        ("Fagg_claim_table[0] == 1", ["agg_claim_table", "claim_amount"], []),
        ("Fagg_claim_table[0][0] == 'v'", ["agg_claim_table", "claim_amount"], []),
        ("Fagg_claim_table > 0", ["agg_claim_table"], ["dep_claim_ref"]),
        ("type_code__agg_claim_table > 0", ["agg_claim_table"], ["dep_claim_ref"]),
        ("Fdep_claim_ref > 0", ["agg_claim_table"], ["dep_claim_ref"]),
        ("Fagg_claim_table > Fdep_claim_ref", ["agg_claim_table", "claim_amount"], ["dep_claim_ref"]),
        ("compare_dates(Fagg_claim_table, Fdep_claim_ref) < 0", ["agg_claim_table", "claim_amount"], ["dep_claim_ref"]),
        ("len(type_code__agg_claim_table) > 0", ["agg_claim_table", "claim_amount"], []),
        ("type_code__item_of__agg_claim_table__1 > 0", ["agg_claim_table", "claim_amount"], []),
        ("int(cell(type_code__agg_claim_table, 0, 0)) == 1", ["agg_claim_table", "claim_amount"], []),
        (
            "check_dependency(type_code__item_of__agg_claim_table__0, type_code__item_of__agg_claim_table__1)",
            ["agg_claim_table", "claim_amount"],
            [],
        ),
        ("Fagg_claim_table[0] == 1", ["agg_claim_table"], ["dep_claim_ref"]),
        ("type_code__agg_claim_table[0] == 1", ["agg_claim_table"], ["dep_claim_ref"]),
        ("check_dependency(Fagg_claim_table__0, Fagg_claim_table__1)", ["agg_claim_table"], ["dep_claim_ref"]),
    ],
)
def test_validate__declared_field_missing_from_rule__raises(
    rule_field_references_validator,
    rule,
    validated_fields,
    dependent_fields,
):
    with pytest.raises(RuleFieldReferencesMismatchError):
        rule_field_references_validator.validate(
            rule=rule,
            validated_fields=validated_fields,
            dependent_fields=dependent_fields,
        )


@pytest.mark.parametrize(
    "rule,validated_fields,dependent_fields",
    [
        ("Ffield1 > Ffield2", ["field1", "field2"], []),
        ("type_code__field1 > type_code__field2", ["field1", "field2"], []),
        ("len(Ffield1) > 0 and Ffield2 != ''", ["field1", "field2"], []),
        ("len(type_code__field1) > 0 and type_code__field2 != ''", ["field1", "field2"], []),
        ("min(Ffield1, Ffield2) >= 0", ["field1", "field2"], []),
        ("Ffield1__0 == Ffield2__1", ["field1", "field2"], []),
        ("Ffield1 > 0 and Fdep_field > 0", ["field1"], ["dep_field"]),
        ("compare_dates(Ffield1, Fdep_field) <= 0", ["field1"], ["dep_field"]),
        ("check_dependency(Ffield1__0, Fdep_field__0)", ["field1"], ["dep_field"]),
        ("Ffield1[0][0] == Ffield2[0][0]", ["field1", "field2"], []),
        ("Fagg_claim_table > Fclaim_amount", ["agg_claim_table", "claim_amount"], []),
        ("type_code__agg_claim_table > type_code__claim_amount", ["agg_claim_table", "claim_amount"], []),
        ("len(Fagg_claim_table) > 0 and Fclaim_amount != ''", ["agg_claim_table", "claim_amount"], []),
        (
            "len(type_code__agg_claim_table) > 0 and type_code__claim_amount != ''",
            ["agg_claim_table", "claim_amount"],
            [],
        ),
        ("min(Fagg_claim_table, Fclaim_amount) >= 0", ["agg_claim_table", "claim_amount"], []),
        ("type_code__agg_claim_table__0 == type_code__claim_amount__1", ["agg_claim_table", "claim_amount"], []),
        ("Fagg_claim_table > 0 and Fdep_claim_ref > 0", ["agg_claim_table"], ["dep_claim_ref"]),
        ("compare_dates(Fagg_claim_table, Fdep_claim_ref) <= 0", ["agg_claim_table"], ["dep_claim_ref"]),
        (
            "check_dependency(type_code__item_of__agg_claim_table__0, type_code__item_of__agg_claim_table__1)",
            ["agg_claim_table"],
            [],
        ),
        ("check_dependency(Fagg_claim_table__0, Fdep_claim_ref__0)", ["agg_claim_table"], ["dep_claim_ref"]),
        (
            (
                "not check_dependency(type_code__item_of__agg_claim_table__1) "
                "or type_code__item_of__agg_claim_table__1 > 0"
            ),
            ["agg_claim_table"],
            [],
        ),
    ],
)
def test_validate__valid_rule_references__no_error(
    rule_field_references_validator,
    rule,
    validated_fields,
    dependent_fields,
):
    rule_field_references_validator.validate(
        rule=rule,
        validated_fields=validated_fields,
        dependent_fields=dependent_fields,
    )
