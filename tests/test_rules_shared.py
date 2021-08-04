# -*- coding: utf-8 -*-

import pytest
from pymarc import Field

from bookops_callno.rules_shared import (
    callno_cutter_fic,
    callno_cutter_initial,
    callno_cutter_pic,
)


@pytest.mark.parametrize(
    "tag,inds,subs,expectation",
    [
        ("100", ["1", " "], ["a", "Adams, John,", "e", "author."], "ADAMS"),
        ("110", ["2", " "], ["a", "Foo."], "F"),
        ("245", ["0", "4"], ["a", "The foo."], "F"),
    ],
)
def test_callno_cutter_fic(tag, inds, subs, expectation):
    field = Field(tag=tag, indicators=inds, subfields=subs)
    assert callno_cutter_fic(field) == expectation


@pytest.mark.parametrize("arg", [None, 100])
def test_callno_cutter_fic_invalid_arg(arg):
    assert callno_cutter_fic(arg) is None


@pytest.mark.parametrize(
    "tag,inds,subs,expectation",
    [
        ("100", ["1", " "], ["a", "Adams, John."], "A"),
        ("110", ["2", " "], ["a", "Foo Company."], "F"),
        ("245", ["0", "4"], ["a", "The foo."], "F"),
        ("246", ["3", " "], ["a", "The spam."], None),
    ],
)
def test_callno_cutter_initial(tag, inds, subs, expectation):
    field = Field(tag=tag, indicators=inds, subfields=subs)
    assert callno_cutter_initial(field) == expectation


@pytest.mark.parametrize("arg", [None, 123])
def test_callno_cutter_initial_invalid_arg(arg):
    assert callno_cutter_initial(arg) is None


@pytest.mark.parametrize(
    "tag,inds,subs,expectation",
    [
        ("100", ["1", " "], ["a", "Adams, John,", "e", "author."], "ADAMS"),
        ("110", ["2", " "], ["a", "Foo Company."], "FOO"),
        ("245", ["0", "4"], ["a", "The foo."], "F"),
    ],
)
def test_callno_cutter_pic(tag, inds, subs, expectation):
    field = Field(tag=tag, indicators=inds, subfields=subs)
    assert callno_cutter_pic(field) == expectation


@pytest.mark.parametrize("arg", [None, 100])
def test_callno_cutter_pic_invalid_arg(arg):
    assert callno_cutter_pic(arg) is None
