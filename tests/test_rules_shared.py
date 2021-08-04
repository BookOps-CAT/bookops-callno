# -*- coding: utf-8 -*-

import pytest
from pymarc import Field

from bookops_callno.rules_shared import callno_cutter_fic, callno_cutter_pic


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
