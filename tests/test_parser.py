# -*- coding: utf-8 -*-

import pytest
from pymarc import Record, Field

from bookops_callno.parser import get_field, has_tag, main_entry_tag
from bookops_callno.errors import CallNoConstructorError


def test_has_tag_exception_no_pymarc_bib():
    msg = "Invalid 'bib' argument used. Must be pymarc.Record instance."
    with pytest.raises(CallNoConstructorError) as exc:
        has_tag("100", "100")
    assert msg in str(exc)


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


def test_main_entry_tag_exception_no_pymarc_bib():
    msg = "Invalid 'bib' argument used. Must be pymarc.Record instance."
    with pytest.raises(CallNoConstructorError) as exc:
        main_entry_tag()
    assert msg in str(exc)


def test_main_entry_tag_100():
    bib = Record()
    bib.add_field(Field(tag="100", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert main_entry_tag(bib) == "100"


def test_main_entry_tag_110():
    bib = Record()
    bib.add_field(Field(tag="110", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert main_entry_tag(bib) == "110"


def test_main_entry_tag_111():
    bib = Record()
    bib.add_field(Field(tag="111", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert main_entry_tag(bib) == "111"


def test_main_entry_tag_245():
    bib = Record()
    bib.add_field(Field(tag="130", indicators=[], subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", indicators=[], subfields=["a", "bar"]))

    assert main_entry_tag(bib) == "245"


def test_main_entry_tag_None():
    bib = Record()
    bib.add_field(Field(tag="130", indicators=[], subfields=["a", "foo"]))

    assert main_entry_tag(bib) is None


def test_get_field_exception_invalid_bib_arg():
    msg = "Invalid 'bib' argument used. Must be pymarc.Record instance."
    with pytest.raises(CallNoConstructorError) as exc:
        get_field(None, "100")
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
