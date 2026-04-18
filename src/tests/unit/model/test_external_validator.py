import pytest

from deps_high_sparrow.domain.model import IllegalArgumentError


@pytest.mark.parametrize(
    "name,is_valid",
    (
        ("1", True),
        ("en", True),
        ("azAZ09-_", True),
        ("Words with spaces", False),
        ("1234#%$(}-", False),
        ("snake_case", True),
        ("Words-with-dashes", True),
        ("Words-with-dashes and spaces", False),
        ("", False),
        ("  ", False),
        ("1" * 101, False),
    ),
)
def test_external_validator_name__checked(name, is_valid, external_validator_factory):
    if is_valid:
        assert external_validator_factory(name=name).name == name
    else:
        with pytest.raises(IllegalArgumentError):
            external_validator_factory(name=name)


@pytest.mark.parametrize(
    "url,is_valid",
    (
        ("http://example.com", True),
        ("https://example.com", True),
        ("ftp://example.com", False),  # FTP is not HTTP/HTTPS
        ("https://sub.domain.com/path?query=123", True),
        ("http://localhost:8080", True),
        ("http://validation", True),
        ("http://high-sparrow:8000", True),
        ("http://-validation:8000", False),  # Invalid leading character
        ("http://validation-:8000", False),  # Invalid trailing character
        ("http://high_sparrow", False),  # Invalid character
        ("https://192.168.0.1", True),
        ("http://123.456.789.000", True),  # Does not check for invalid IP
        ("https://.com", False),  # Invalid domain name
        ("http://-example.com", False),  # Invalid character in domain
        ("https://example.com:8080/path", True),
        ("http://test.com/page?name=abc#section", True),
        ("http://[::1]:8080", False),  # Does not support IPv6 URL
        ("https://example..com", False),  # Double dot in domain
        ("https://-example.com", False),  # Invalid leading character
        ("http://example.c", False),  # Invalid TLD
        ("http://example-.com", False),  # Invalid trailing character
        ("http://example.com/path//double", True),  # Double slashes in path are valid
        ("https://123.1", False),  # Invalid IP format
        ("https://www.example.com/path#fragment", True),
    ),
)
def test_external_validator_url__checked(url, is_valid, external_validator_factory):
    if is_valid:
        assert external_validator_factory(url=url).url == url
    else:
        with pytest.raises(IllegalArgumentError):
            external_validator_factory(url=url)
