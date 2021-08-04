# -*- coding: utf-8 -*-

from pymarc import Field
import pytest


from bookops_callno.rules_bpl import callno_format_prefix


@pytest.mark.parametrize(
    "rec_type,form,expectation",
    [
        ("a", "o", "eBOOK"),
        ("a", "s", "eBOOK"),
        ("t", "o", "eBOOK"),
        ("t", "s", "eBOOK"),
        ("a", "a", "NM"),
        ("a", "b", "NM"),
        ("c", " ", "Mu"),
        ("d", " ", "Mu"),
        ("a", " ", None),
        ("t", " ", None),
        ("i", "o", "eAUDIO"),
        ("i", "s", "eAUDIO"),
        ("i", " ", "AUDIO"),
        ("j", "o", "eMUSIC"),
        ("j", "s", "eMUSIC"),
        ("j", " ", "CD"),
        ("g", "o", "eVIDEO"),
        ("g", "s", "eVIDEO"),
        ("g", " ", "DVD"),
        ("k", None, None),
    ],
)
def test_callno_format_prefix(rec_type, form, expectation):
    assert callno_format_prefix(rec_type, form) == expectation


@pytest.mark.parametrize(
    "rec_type,form,sub,expectation",
    [("a", " ", "Librettos.", "LIB"), ("a", " ", "Fiction.", None)],
)
def test_callno_format_prefix_librettos(rec_type, form, sub, expectation):
    subjs = [Field(tag="650", indicators=[" ", "0"], subfields=["a", "Foo", "v", sub])]
    assert callno_format_prefix(rec_type, form, subjs) == expectation
