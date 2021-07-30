# -*- coding: utf-8 -*-

import pytest

from bookops_callno.errors import CallNoConstructorError
from bookops_callno.normalizer import normalize_value


@pytest.mark.parametrize("arg", [None, ""])
def test_normalize_value_empty_value(arg):
    assert normalize_value(arg) == ""


def test_normalize_value_invalid_type_exception():
    msg = "Invalid 'value' type used in argument. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        normalize_value(123)
    assert msg in str(exc)


def test_normalize_value_unidecode_exception():
    msg = "Unsupported character encountered. Error: "
    with pytest.raises(CallNoConstructorError) as exc:
        normalize_value("\ue000")
    assert msg in str(exc)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("Foo", "FOO"),
        ("ĄąĆćĘęŁłŃńÓóŚśŹźŻż", "AACCEELLNNOOSSZZZZ"),
        ("ÁáÉéÍíÑñÓóÚúý", "AAEEIINNOOUUY"),
        ("ÄäËëḦḧÏïÖöẗÜüṲṳẄẅẌẍŸÿ", "AAEEHHIIOOTUUUUWWXXYY"),
        ("Metlit︠s︡kai︠a︡, Marii︠a︡.", "METLITSKAIA, MARIIA."),
        ("szegfű és fahéj", "SZEGFU ES FAHEJ"),
    ],
)
def test_normalize_value(arg, expectation):
    assert normalize_value(arg) == expectation
