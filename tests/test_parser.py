# -*- coding: utf-8 -*-

import pytest
from pymarc import Record, Field

from bookops_callno.parser import (
    get_field,
    get_language_code,
    get_main_entry_tag,
    get_audience,
    has_audience_code,
    has_tag,
    is_short,
)
from bookops_callno.errors import CallNoConstructorError


def test_get_audience_none_bib():
    assert get_audience(bib=None) is None


def test_get_audience_invalid_record_type():
    bib = Record()
    bib.leader = "@" * 6 + "as"
    assert get_audience(bib=bib) is None


@pytest.mark.parametrize(
    "arg, expectation",
    [
        ("@" * 22 + "a", "early juv"),
        ("@" * 22 + "b", "early juv"),
        ("@" * 22 + "c", "juv"),
        ("@" * 22 + "j", "juv"),
        ("@" * 22 + "d", "young adult"),
        ("@" * 22 + " ", "adult"),
    ],
)
def test_get_audience_008_tag_only(arg, expectation):
    bib = Record()
    bib.leader = "@" * 6 + "am"  # leader for print monograph material
    bib.add_field(Field(tag="008", data=arg))
    assert get_audience(bib) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (
            "1 volume: ",
            "early juv",
        ),
        ("28 pages: ", "early juv"),
        ("124 pages: ", "juv"),
    ],
)
def test_get_audience_short_book(arg, expectation):
    bib = Record()
    bib.leader = "@" * 6 + "am"
    bib.add_field(
        Field(
            tag="008",
            data="@" * 22 + "j",
        )
    )
    bib.add_field(Field(tag="300", indicators=[], subfields=["a", arg]))
    assert get_audience(bib) == expectation


def test_get_language_code_none_bib():
    assert get_language_code() is None


def test_get_language_code_no_008_tag():
    bib = Record()
    assert get_language_code(bib=bib) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [("@" * 35 + "rus", "rus"), ("@" * 35 + "ENG", "eng"), ("@", None)],
)
def test_get_languge_code(arg, expectation):
    bib = Record()
    bib.add_field(Field(tag="008", data=arg))
    assert get_language_code(bib=bib) == expectation


def test_get_main_entry_tag_none_bib():
    assert get_main_entry_tag(bib=None) is None


def test_get_main_entry_tag_exception_invalid_bib_obj():
    msg = "Invalid 'bib' argument used. Must be pymarc.Record instance."
    with pytest.raises(CallNoConstructorError) as exc:
        get_main_entry_tag(bib="foo")
    assert msg in str(exc)


def test_get_main_entry_tag_100():
    bib = Record()
    bib.add_field(Field(tag="100", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert get_main_entry_tag(bib) == "100"


def test_get_main_entry_tag_110():
    bib = Record()
    bib.add_field(Field(tag="110", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert get_main_entry_tag(bib) == "110"


def test_get_main_entry_tag_111():
    bib = Record()
    bib.add_field(Field(tag="111", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert get_main_entry_tag(bib) == "111"


def test_get_main_entry_tag_245():
    bib = Record()
    bib.add_field(Field(tag="130", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert get_main_entry_tag(bib) == "245"


def test_get_main_entry_tag_None():
    bib = Record()
    bib.add_field(Field(tag="130", indicators=[], subfields=["a", "foo"]))

    assert get_main_entry_tag(bib) is None


def test_get_field_none_bib():
    assert get_field(bib=None, tag="100") is None


def test_get_field_exception_invalid_bib_arg():
    msg = "Invalid 'bib' argument used. Must be pymarc.Record instance."
    with pytest.raises(CallNoConstructorError) as exc:
        get_field("foo", "100")
    assert msg in str(exc)


def test_get_field_exception_invalid_tag_arg():
    msg = "Invalid 'tag' argument used. Must be string."
    with pytest.raises(CallNoConstructorError) as exc:
        bib = Record()
        get_field(bib, 100)
    assert msg in str(exc)


def test_get_field_missing_field():
    bib = Record()
    assert get_field(bib, "100") is None


def test_get_field_success():
    bib = Record()
    bib.add_field(Field(tag="100", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="100", indicators=[], subfields=["a", "bar"]))
    field = get_field(bib, "100")
    assert type(field) == Field
    assert field.tag == "100"
    assert field.indicators == []
    assert field.subfields == ["a", "foo"]


def test_has_audience_code_invalid_leader():
    msg = "Invalid 'leader' type used in argument. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        has_audience_code(123)
    assert msg in str(exc)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (None, False),
        ("foo", False),
        ("@" * 6 + "aa", True),
        ("@" * 6 + "am", True),
        ("@" * 6 + "ca", True),
        ("@" * 6 + "cm", True),
        ("@" * 6 + "da", True),
        ("@" * 6 + "dm", True),
        ("@" * 6 + "ga", True),
        ("@" * 6 + "gm", True),
        ("@" * 6 + "ia", True),
        ("@" * 6 + "im", True),
        ("@" * 6 + "ja", True),
        ("@" * 6 + "jm", True),
        ("@" * 6 + "ka", True),
        ("@" * 6 + "km", True),
        ("@" * 6 + "ma", True),
        ("@" * 6 + "mm", True),
        ("@" * 6 + "ta", True),
        ("@" * 6 + "tm", True),
    ],
)
def test_has_audience_code(arg, expectation):
    """
    Tests possible combinations of record types that
    have audience code in position 22 of the 008 tag
    """
    assert has_audience_code(arg) == expectation


def test_has_tag_exception_no_pymarc_bib():
    assert not has_tag(bib=None, tag="100")


def tes_has_tag_exception_invalid_tag():
    msg = "Invalid 'tag' argument used. Must be string."
    with pytest.raises(CallNoConstructorError) as exc:
        has_tag("100", 100)
    assert msg in str(exc)


def test_has_tag_false():
    bib = Record()
    assert not has_tag(bib, "100")


def test_has_tag_true():
    bib = Record()
    bib.add_field(Field(tag="100", indicators=["1", " "], subfields=["a", "Foo"]))
    assert has_tag(bib, "100")


def test_is_short_none_bib():
    assert is_short(bib=None) is None


def test_is_short_bib_without_300():
    bib = Record()
    assert is_short(bib=bib) is None


def test_is_short_bib_wwithout_sub_a_in_300():
    bib = Record()
    bib.add_field(Field(tag="300", indicators=[], subfields=["b", "foo"]))
    assert is_short(bib=bib) is None


@pytest.mark.parametrize(
    "arg, expectation",
    [
        ("1 volumne (unpaged) :", True),
        ("1 v. (unpaged): ", True),
        ("v. :", False),
        ("volumes :", False),
        ("23 pages :", True),
        ("50 pages :", False),
        ("xv,23 pages :", False),
        ("245 pages :", False),
    ],
)
def test_is_short(arg, expectation):
    bib = Record()
    bib.add_field(Field(tag="300", indicators=[], subfields=["a", arg]))
    assert is_short(bib=bib) == expectation
