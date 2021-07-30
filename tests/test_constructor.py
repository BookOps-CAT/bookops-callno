# -*- coding: utf-8 -*-

from pymarc import Record, Field
import pytest


from bookops_callno.constructor import CallNo, BplCallNo
from bookops_callno.errors import CallNoConstructorError


def test_CallNo_none_bib():
    cn = CallNo(bib=None)
    assert cn.audience_info is None
    assert cn.content_info is None
    assert cn.cutter_info is None
    assert cn.language_info is None
    assert cn.physical_desc_info is None
    assert cn.record_type_info is None
    assert cn.subject_info == []
    assert cn.callno_field is None
    assert cn.requested_call_type == "auto"


def test_CallNo_exception_invalid_requested_call_type():
    msg = "Invalid type of 'requested_call_type' argument used. Must be a string."
    with pytest.raises(CallNoConstructorError) as exc:
        bib = Record()
        CallNo(bib=bib, requested_call_type=1)
    assert msg in str(exc)


@pytest.mark.parametrize(
    "arg,expectation",
    [("a", "early juv"), ("j", "juv"), ("d", "young adult"), (" ", "adult")],
)
def test_CallNo_get_audience_info(arg, expectation):
    cn = CallNo(bib=None)
    bib = Record()
    bib.leader = "@" * 6 + "am"
    bib.add_field(Field(tag="008", data="@" * 22 + arg))
    assert cn._get_audience_info(bib=bib) == expectation


def test_CallNo_get_form_of_item_info():
    cn = CallNo()
    bib = Record()
    bib.leader = "@" * 6 + "am"
    bib.add_field(Field(tag="008", data="@" * 23 + "a"))
    assert cn._get_form_of_item_info(bib) == "a"


def test_CallNo_get_language_info():
    cn = CallNo()
    bib = Record()
    bib.leader = "@" * 6 + "am"
    bib.add_field(Field(tag="008", data="@" * 35 + "spa"))
    assert cn._get_language_info(bib) == "spa"


def test_CallNo_main_entry_100_tag():
    callno = CallNo(bib=None)
    bib = Record()
    bib.add_field(Field(tag="100", subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", subfields=["a", "bar"]))
    field = callno._get_main_entry_info(bib)
    assert type(field) == Field
    assert str(field) == "=100  $afoo"
    assert field.tag == "100"


def test_CallNo_main_entry_110_tag():
    callno = CallNo(bib=None)
    bib = Record()
    bib.add_field(Field(tag="110", subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", subfields=["a", "bar"]))
    field = callno._get_main_entry_info(bib)
    assert type(field) == Field
    assert str(field) == "=110  $afoo"
    assert field.tag == "110"


def test_CallNo_main_entry_245_tag():
    callno = CallNo(bib=None)
    bib = Record()
    bib.add_field(Field(tag="130", subfields=["a", "foo"]))
    bib.add_field(Field(tag="245", subfields=["a", "bar"]))
    field = callno._get_main_entry_info(bib)
    assert type(field) == Field
    assert str(field) == "=245  $abar"
    assert field.tag == "245"


def test_CallNo_get_physical_description():
    cn = CallNo()
    bib = Record()
    bib.add_field(
        Field(tag="300", subfields=["a", "1 volume:", "b", "maps;", "c", "20 cm"])
    )
    assert cn._get_physical_description_info(bib) == "1 volume: maps; 20 cm"


def test_CallNo_get_record_type_info():
    cn = CallNo()
    bib = Record()
    bib.leader = "@" * 6 + "a"
    assert cn._get_record_type_info(bib) == "a"


def test_CallNo_get_subject_info():
    cn = CallNo(bib=None)
    bib = Record()
    bib.add_field(Field(tag="600", indicators=[" ", "7"], subfields=["a", "Foo."]))
    bib.add_field(Field(tag="600", indicators=["1", "0"], subfields=["a", "Bar."]))
    bib.add_field(Field(tag="650", indicators=[" ", "0"], subfields=["a", "Spam."]))
    bib.add_field(Field(tag="690", indicators=[" ", "0"], subfields=["a", "Eggs."]))
    res = cn._get_subject_info(bib)
    assert len(res) == 2
    for r in res:
        assert type(r) == Field
    assert res[0].value() == "Bar."
    assert res[1].value() == "Spam."


def test_CallNo_as_pymarc_field():
    cn = CallNo(bib=None)
    cn.callno_field = "foo"
    assert cn.as_pymarc_field() == "foo"


@pytest.mark.parametrize(
    "arg,expectation", [(None, ""), (Field(tag="091", subfields=["a", "FOO"]), "FOO")]
)
def test_CallNo_repr(arg, expectation):
    cn = CallNo(bib=None)
    cn.callno_field = arg
    assert str(cn) == expectation


def test_BplCallNo_initiation():
    bcn = BplCallNo()
    assert bcn.audience_info is None
    assert bcn.content_info is None
    assert bcn.cutter_info is None
    assert bcn.language_info is None
    assert bcn.physical_desc_info is None
    assert bcn.record_type_info is None
    assert bcn.subject_info == []
    assert bcn.callno_field is None
    assert bcn.requested_call_type == "auto"
    assert bcn.tag == "099"
    assert bcn.inds == [" ", " "]


def test_BplCallNo_eaudio():
    bcn = BplCallNo(requested_call_type="eaudio")
    cf = bcn.as_pymarc_field()
    assert cf.tag == "099"
    assert cf.indicators == [" ", " "]
    assert cf.subfields == ["a", "eAUDIO"]


def test_BplCallNo_ebook():
    bcn = BplCallNo(requested_call_type="ebook")
    cf = bcn.as_pymarc_field()
    assert cf.tag == "099"
    assert cf.indicators == [" ", " "]
    assert cf.subfields == ["a", "eBOOK"]


def test_BplCallNo_evideo():
    bcn = BplCallNo(requested_call_type="evideo")
    cf = bcn.as_pymarc_field()
    assert cf.tag == "099"
    assert cf.indicators == [" ", " "]
    assert cf.subfields == ["a", "eVIDEO"]
