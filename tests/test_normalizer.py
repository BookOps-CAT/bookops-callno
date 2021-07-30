# -*- coding: utf-8 -*-

from pymarc import Field
import pytest

from bookops_callno.errors import CallNoConstructorError
from bookops_callno.normalizer import (
    corporate_name_first_word,
    corporate_name_full,
    corporate_name_initial,
    normalize_value,
    personal_name_initial,
    personal_name_surname,
    remove_trailing_punctuation,
)


def test_corporate_name_first_word_none_field():
    assert corporate_name_first_word(field=None) is None


def test_corporate_name_first_word_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        corporate_name_first_word(field=1)
    assert msg in str(exc)


def test_corporate_name_first_word_invalid_tag():
    field = Field(tag="710", indicators=["2", "0"], subfields=["a", "Foo."])
    assert corporate_name_first_word(field=field) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (["a", "United States.", "b", "Army."], "UNITED"),
        (["a", "Poland.", "b", "Army."], "POLAND"),
        (["a", "Green Day (Musical group)"], "GREEN"),
    ],
)
def test_corporate_name_first_word(arg, expectation):
    field = Field(tag="110", indicators=["2", "0"], subfields=arg)
    assert corporate_name_first_word(field=field) == expectation


def test_corporate_name_full_none_field():
    assert corporate_name_full(field=None) is None


def test_corporate_name_full_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        corporate_name_full(field=1)
    assert msg in str(exc)


def test_corporate_name_full_invalid_tag():
    field = Field(tag="710", indicators=["2", "0"], subfields=["a", "Foo."])
    assert corporate_name_full(field=field) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (["a", "United States.", "b", "Army."], "UNITED STATES"),
        (["a", "Green Day (Musical group)"], "GREEN DAY"),
    ],
)
def test_corporate_name_full(arg, expectation):
    field = Field(tag="110", indicators=["2", "0"], subfields=arg)
    assert corporate_name_full(field=field) == expectation


def test_corporate_name_initial_none_field():
    assert corporate_name_initial(field=None) is None


def test_corporate_name_initial_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        corporate_name_initial(field=1)
    assert msg in str(exc)


def test_corporate_name_initial_invalid_tag():
    field = Field(tag="710", indicators=["2", "0"], subfields=["a", "Foo."])
    assert corporate_name_initial(field=field) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [(["a", "United States.", "b", "Army."], "U"), (["a", "Äu"], "A")],
)
def test_corporate_name_initial(arg, expectation):
    field = Field(tag="110", indicators=["2", "0"], subfields=arg)
    assert corporate_name_initial(field=field) == expectation


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
        ("Metlit︠s︡kai︠a︡, Marii︠a︡.", "METLITSKAIA, MARIIA"),
        ("szegfű és fahéj", "SZEGFU ES FAHEJ"),
    ],
)
def test_normalize_value(arg, expectation):
    assert normalize_value(arg) == expectation


def test_personal_name_initial_none_field():
    assert personal_name_initial(field=None) is None


def test_personal_name_initial_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        personal_name_initial(12)
    assert msg in str(exc)


def test_personal_name_initial_wrong_field_tag():
    field = Field(tag="600", indicators=["1", " "], subfields=["a", "foo."])
    assert personal_name_initial(field=field) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [(["a", "Adams, John."], "A"), (["a", "Łowca, Jan,", "e", "author"], "L")],
)
def test_personal_name_initial(arg, expectation):
    field = Field(tag="100", indicators=["1", " "], subfields=arg)
    assert personal_name_initial(field=field) == expectation


def test_remove_trailing_puncutation_invalid_type_exception():
    msg = "Invalid 'value' type used in argument. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        remove_trailing_punctuation(value=None)
    assert msg in str(exc)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("foo", "foo"),
        ("foo.", "foo"),
        ("foo... ", "foo"),
        ("foo-", "foo"),
        ("foo, ", "foo"),
        ("foo; ", "foo"),
        ("foo (", "foo"),
        ("foo: ", "foo"),
    ],
)
def test_remove_trailing_puncutation(arg, expectation):
    assert remove_trailing_punctuation(arg) == expectation
