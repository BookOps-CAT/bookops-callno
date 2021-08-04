# -*- coding: utf-8 -*-

from pymarc import Record, Field
import pytest

from bookops_callno.constructor_bpl import BplCallNo


def test_BplCallNo_initiation():
    bcn = BplCallNo()
    assert bcn.audience_info is None
    assert bcn.content_info is None
    assert bcn.cutter_info is None
    assert bcn.language_code is None
    assert bcn.physical_desc_info is None
    assert bcn.record_type_info is None
    assert bcn.subject_info == []
    assert bcn.callno_field is None
    assert bcn.requested_call_type == "auto"
    assert bcn.tag == "099"
    assert bcn.inds == [" ", " "]


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ([], []),
        ([None, "foo", None], ["foo"]),
        ([None, None], []),
        (["foo", None, "bar"], ["foo", "bar"]),
        (["", "foo"], ["foo"]),
    ],
)
def test_BplCallNo_cleanup_callno_elements(arg, expectation):
    bcn = BplCallNo()
    assert bcn._cleanup_callno_elements(arg) == expectation


def test_BplCallNo_create_eaudio_callno():
    bcn = BplCallNo(requested_call_type="eaudio")
    cf = bcn.as_pymarc_field()
    assert cf.tag == "099"
    assert cf.indicators == [" ", " "]
    assert cf.subfields == ["a", "eAUDIO"]


def test_BplCallNo_create_ebook_callno():
    bcn = BplCallNo(requested_call_type="ebook")
    cf = bcn.as_pymarc_field()
    assert cf.tag == "099"
    assert cf.indicators == [" ", " "]
    assert cf.subfields == ["a", "eBOOK"]


def test_BplCallNo_crate_evideo_callno():
    bcn = BplCallNo(requested_call_type="evideo")
    cf = bcn.as_pymarc_field()
    assert cf.tag == "099"
    assert cf.indicators == [" ", " "]
    assert cf.subfields == ["a", "eVIDEO"]


def test_BplCallNo_construct_subfields():
    bcn = BplCallNo()
    assert bcn._construct_subfields(["foo", "bar", "baz"]) == [
        "a",
        "foo",
        "a",
        "bar",
        "a",
        "baz",
    ]


def test_BplCallNo_create_fic_callno_invalid_data():
    bcn = BplCallNo()
    bcn.mat_format = None
    bcn.langugage_code = None
    bcn.audience_info = "adult"
    bcn.cutter_info = Field(tag="111", indicators=["1", " "], subfields=["a", "Foo."])
    assert bcn._create_fic_callno() is None


@pytest.mark.parametrize(
    "form,lang,audn,main_entry_tag,main_entry_ind, main_entry_subs,expectation",
    [
        (
            "print",
            None,
            "adult",
            "100",
            ["1", " "],
            ["a", "Adams, John,", "e", "author."],
            "=099  \\\\$aFIC$aADAMS",
        ),
        (
            "print",
            "CHI",
            "adult",
            "100",
            ["1", " "],
            ["a", "Adams, John,", "e", "author."],
            "=099  \\\\$aCHI$aFIC$aADAMS",
        ),
        (
            "print",
            None,
            "juv",
            "100",
            ["0", ""],
            ["a", "Aesop."],
            "=099  \\\\$aJ$aFIC$aAESOP",
        ),
        (
            "audio",
            None,
            "juv",
            "100",
            ["1", " "],
            ["a", "Adams, John,", "e", "author."],
            "=099  \\\\$aAUDIO$aJ$aFIC$aADAMS",
        ),
        (
            "print",
            "CHI",
            "young adult",
            "110",
            ["2", "0"],
            ["a", "Foo."],
            "=099  \\\\$aCHI$aFIC$aF",
        ),
        (
            "print",
            None,
            "adult",
            "245",
            ["0", "4"],
            ["a", "The Foo."],
            "=099  \\\\$aFIC$aF",
        ),
        (
            "print",
            None,
            "adult",
            "100",
            ["3", " "],
            ["a", "Adams (Family :", "d", "1872-1963 :", "c", "South Africa)"],
            "None",
        ),
    ],
)
def test_BplCallNo_create_fic_callno(
    form, lang, audn, main_entry_tag, main_entry_ind, main_entry_subs, expectation
):
    bcn = BplCallNo()
    bcn.mat_format = form
    bcn.language_code = lang
    bcn.audience_info = audn
    bcn.cutter_info = Field(
        tag=main_entry_tag, indicators=main_entry_ind, subfields=main_entry_subs
    )
    assert str(bcn._create_fic_callno()) == expectation


def test_BplCallNo_create_pic_callno_invalid_data():
    bcn = BplCallNo()
    bcn.language_code = None
    bcn.audience_info = "adult"
    bcn.cutter_info = Field(tag="111", indicators=[" ", " "], subfields=["a", "Foo."])
    assert bcn._create_pic_callno() is None


@pytest.mark.parametrize(
    "lang,main_entry_tag,main_entry_ind,main_entry_subs,expectation",
    [
        (
            None,
            "100",
            ["1", " "],
            ["a", "Adams, John,", "e", "author."],
            "=099  \\\\$aJ-E$aADAMS",
        ),
        (None, "110", ["2", " "], ["a", "Foo Company."], "=099  \\\\$aJ-E$aFOO"),
        (
            None,
            "245",
            ["0 ", "4"],
            ["a", "The foo /", "c", "Spam."],
            "=099  \\\\$aJ-E$aF",
        ),
        (
            "CHI",
            "100",
            ["1", " "],
            ["a", "Foo, Spam,", "e", "author."],
            "=099  \\\\$aCHI$aJ-E$aFOO",
        ),
    ],
)
def test_BplCallNo_create_pic_callno(
    lang, main_entry_tag, main_entry_ind, main_entry_subs, expectation
):
    bcn = BplCallNo()
    bcn.language_code = lang
    bcn.cutter_info = Field(
        tag=main_entry_tag, indicators=main_entry_ind, subfields=main_entry_subs
    )
    assert str(bcn._create_pic_callno()) == expectation


# @pytest.mark.parametrize(
#     "lang,main_entry_tag,main_entry_ind,main_entry_subs,subj,expectation"
# )
# def test_BplCallNo_create_bio_callno(
#     lang, main_entry_tag, main_entry_ind, main_entry_subs, subj
# ):
#     pass
