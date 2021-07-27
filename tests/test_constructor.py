# -*- coding: utf-8 -*-

from collections import namedtuple

from pymarc import Record, Field
import pytest


from bookops_callno.constructor import CallNo, MainEntry
from bookops_callno.errors import CallNoConstructorError


def test_CallNo_none_bib():
    cn = CallNo(bib=None, library="bpl")
    assert cn.library == "bpl"
    assert cn.call_type_requested == "auto"
    assert cn.call_type_produced is None
    assert cn.segment_audn is None
    assert cn.segment_content is None
    assert cn.segment_cutter is None
    assert cn.segment_format is None
    assert cn.segment_language is None
    assert cn.segment_subject is None


def test_CallNo_exception_invalid_library_type():
    msg = "Invalid type of 'library' argument used. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        bib = Record()
        CallNo(bib=bib, library=1)
    assert msg in str(exc)


def test_CallNo_exeption_invalid_library_value():
    msg = "Invalid 'library' value. Use 'bpl' or 'nypl'."
    with pytest.raises(CallNoConstructorError) as exc:
        bib = Record()
        CallNo(bib=bib, library="foo")
    assert msg in str(exc)


def test_CallNo_exception_invalid_requested_call_type():
    msg = "Invalid type of 'requested_call_type' argument used. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        bib = Record()
        CallNo(bib=bib, library="bpl", requested_call_type=1)
    assert msg in str(exc)


@pytest.mark.parametrize("arg", ["bpl", "nypl", "nyp"])
def test_CallNo_main_entry(arg):
    callno = CallNo(bib=None, library=arg)
    bib = Record()
    bib.add_field(Field(tag="100", subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", subfields=["a", "bar"]))
    field = callno._get_main_entry(bib)
    assert type(field) == Field
    assert str(field) == "=100  $afoo"
    assert field.tag == "100"
