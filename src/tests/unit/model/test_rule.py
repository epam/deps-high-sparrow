import pytest

from deps_high_sparrow.domain.model import IllegalArgumentError


@pytest.mark.parametrize(
    "name,is_valid",
    (
        ("1", True),
        ("1" * 100, True),
        ("", False),
        ("1" * 101, False),
    ),
)
def test_rule_name(name: str, is_valid: bool, rule_factory):
    if is_valid:
        assert rule_factory(name=name).name == name
    else:
        with pytest.raises(IllegalArgumentError):
            rule_factory(name=name)
