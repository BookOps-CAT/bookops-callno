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
    subject_corporate_name,
    subject_family_name,
    subject_personal_name,
    subject_topic,
    title_first_word,
    title_initial,
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
    "arg1,arg2,expectation",
    [
        ("110", ["a", "United States.", "b", "Army."], "UNITED STATES"),
        ("610", ["a", "Green Day (Musical group)"], "GREEN DAY"),
    ],
)
def test_corporate_name_full(arg1, arg2, expectation):
    field = Field(tag=arg1, indicators=["2", "0"], subfields=arg2)
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
        ("Bilʹzho, Andreĭ", "BILZHO, ANDREI"),
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


def test_personal_name_surname_none_field():
    assert personal_name_surname(field=None) is None


def test_personal_name_surname_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        personal_name_surname(123)
    assert msg in str(exc)


def test_personal_name_surname_invalid_tag():
    field = Field(tag="700", indicators=["1", " "], subfields=["a", "Foo."])
    assert personal_name_surname(field=field) is None


@pytest.mark.parametrize(
    "arg1,arg2,expectation",
    [
        ("100", ["a", "Adams, John,", "e", "author."], "ADAMS"),
        ("600", ["a", "Adams, John,", "e", "author."], "ADAMS"),
        (
            "100",
            ["a", "Louis", "b", "XIV,", "c", "King of France,", "d", "1638-1715"],
            "LOUIS XIV",
        ),
        ("100", ["a", "Adams."], "ADAMS"),
        ("100", ["a", "O'Brian, Tim, $e author."], "OBRIAN"),
        (
            "100",
            [
                "a",
                "Aksakova-Sivers, T. A.",
                "q",
                "(Tatʹi︠a︡na Aleksandrovna),",
                "d",
                "1892-1982,",
                "e",
                "author.",
            ],
            "AKSAKOVA-SIVERS",
        ),
        (
            "600",
            ["a", "Pasero de Corneliano, Charles,", "c", "comte,", "d", "1790-1852."],
            "PASERO DE CORNELIANO",
        ),
    ],
)
def test_personal_name_surname(arg1, arg2, expectation):
    field = Field(tag=arg1, indicators=["1", " "], subfields=arg2)
    assert personal_name_surname(field=field) == expectation


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


def test_subject_corporate_name_none_field():
    assert subject_corporate_name(field=None) is None


def test_subject_corporate_name_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        subject_corporate_name(field=610)
    assert msg in str(exc)


def test_subject_corporate_name_wrong_tag():
    field = Field(tag="600", subfields=["a", "foo"])
    assert subject_corporate_name(field=field) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (["a", "Bad Brains (Musical group)"], "BAD BRAINS"),
        (["a", "Cream (Musical group)"], "CREAM"),
    ],
)
def test_subject_corporate_name(arg, expectation):
    field = Field(tag="610", indicators=[" ", "0"], subfields=arg)
    assert subject_corporate_name(field=field) == expectation


def test_subject_family_name_none_field():
    assert subject_family_name(field=None) is None


def test_subject_family_name_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        subject_family_name(field=600)
    assert msg in str(exc)


def test_subject_family_name_invalid_tag():
    field = Field(tag="100", indicators=["3", " "], subfields=["a", "foo"])
    assert subject_family_name(field=field) is None


def test_subject_family_name_invalid_indicator():
    field = Field(tag="600", indicators=["1", "0"], subfields=["a", "foo"])
    assert subject_family_name(field=field) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (["a", "Kennedy family."], "KENNEDY"),
        (["a", "Van Cortlandt family."], "VAN CORTLANDT"),
        (["a", "ʻAlam family."], "ALAM"),
        (["a", "Adams."], None),
    ],
)
def test_subject_family_name(arg, expectation):
    field = Field(tag="600", indicators=["3", "0"], subfields=arg)
    assert subject_family_name(field=field) == expectation


def test_subject_personal_name_none_field():
    assert subject_personal_name(field=None) is None


def test_subject_personal_name_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        subject_personal_name(field=600)
    assert msg in str(exc)


def test_subject_personal_name_invalid_field_indicators():
    field = Field(tag="600", indicators=[" ", "0"], subfields=["a", "foo"])
    assert subject_personal_name(field=field) is None


@pytest.mark.parametrize(
    "arg1,arg2,expectation",
    [
        ("0", ["a", "Adam."], "ADAM"),
        ("1", ["a", "Adams, John,", "x", "Early life."], "ADAMS"),
        (
            "0",
            ["a", "Louis", "b", "XIV,", "c", "King of France,", "d", "1638-1715"],
            "LOUIS XIV",
        ),
    ],
)
def test_subject_personal_name(arg1, arg2, expectation):
    field = Field(tag="600", indicators=[arg1, "0"], subfields=arg2)
    assert subject_personal_name(field=field) == expectation


def test_title_initial_none_field():
    assert title_initial(field=None) is None


def test_title_initial_invalid_field_type():
    msg = "Invalid 'field' argument type. Must be pymarc.Field instance."
    with pytest.raises(CallNoConstructorError) as exc:
        title_initial(field=245)
    assert msg in str(exc)


def test_title_initial_invalid_tag():
    field = Field(tag="246", subfields=["a", "foo"])
    assert title_initial(field=field) is None


@pytest.mark.parametrize(
    "arg1,arg2,expectation",
    [
        ("0", ["a", "Foo."], "F"),
        ("4", ["a", "The foo."], "F"),
        ("2", ["a", "A foo."], "F"),
        (" ", ["Foo"], None),
    ],
)
def test_title_initial(arg1, arg2, expectation):
    field = Field(tag="245", indicators=["0", arg1], subfields=arg2)
    assert title_initial(field=field) == expectation
