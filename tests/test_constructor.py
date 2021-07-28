# -*- coding: utf-8 -*-

from pymarc import Record, Field
import pytest


from bookops_callno.constructor import CallNo
from bookops_callno.errors import CallNoConstructorError


def test_CallNo_none_bib():
    cn = CallNo(bib=None)
    assert cn.audience_info is None
    assert cn.content_info is None
    assert cn.cutter_info is None
    assert cn.format_info is None
    assert cn.language_info is None
    assert cn.subject_info is None


def test_CallNo_exception_invalid_requested_call_type():
    msg = "Invalid type of 'requested_call_type' argument used. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        bib = Record()
        CallNo(bib=bib, requested_call_type=1)
    assert msg in str(exc)


def test_CallNo_main_entry():
    callno = CallNo(bib=None)
    bib = Record()
    bib.add_field(Field(tag="100", subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", subfields=["a", "bar"]))
    field = callno._get_main_entry(bib)
    assert type(field) == Field
    assert str(field) == "=100  $afoo"
    assert field.tag == "100"
