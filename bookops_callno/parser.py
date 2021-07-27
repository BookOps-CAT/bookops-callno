# -*- coding: utf-8 -*-

"""
This module contains methods to parse MARC records in a form of pymarc.Record objects
"""

from typing import Optional

from pymarc import Record, Field


from bookops_callno.errors import CallNoConstructorError


def has_audience_code(leader: str = None) -> bool:
    """
    Determines if MARC record has audience code in position 22 in
    the leader

    Args:
        leader:                 MARC leader field

    Returns:
        boolean
    """
    if leader is None:
        return False
    elif not isinstance(leader, str):
        raise CallNoConstructorError(
            "Invalid 'leader' type used in argument. Must be a string."
        )

    try:
        if leader[6] in ("a", "c", "d", "g", "i", "j", "k", "m", "t") and leader[7] in (
            "a",
            "m",
        ):
            return True
    except IndexError:
        return False


def get_audience(bib: Record = None) -> Optional[str]:
    """
    Determines audience based on MARC 008 tag.
    Possible returns: 'early juv', 'juv', 'young adult', 'adult'.

    Args:
        bib:                    pymarc.Record instance

    Returns:
        audn_code
    """
    if bib is None:
        return None

    # determine has correct bib format
    if not has_audience_code(bib.leader):
        return None

    code = bib["008"].data[22]
    if code in ("a", "b"):
        return "early juv"
    elif code in "c":
        return "juv"
    elif code == "j":
        if is_short(bib):
            return "early juv"
        else:
            return "juv"
    elif code == "d":
        return "young adult"
    else:
        return "adult"


def get_main_entry_tag(bib: Record = None) -> Optional[str]:
    """
    Determines MARC tag of the main entry

    Args:
        bib:                    pymarc.Record instance

    Returns:
        tag
    """
    if bib is None:
        return None
    elif not isinstance(bib, Record):
        raise CallNoConstructorError(
            "Invalid 'bib' argument used. Must be pymarc.Record instance."
        )

    entry_tags = ["100", "110", "111", "245"]

    for tag in entry_tags:
        if has_tag(bib, tag):
            return tag


def get_field(bib: Record = None, tag: str = None) -> Optional[Field]:
    """
    Returns pymarc.Field instance of the the first given MARC tag in a bib

    Args:
        bib:                    pymarc.Record instance
        tag:                    MARC tag as str

    Returns:
        pymarc.Field instance
    """
    if bib is None:
        return None
    elif not isinstance(bib, Record):
        raise CallNoConstructorError(
            "Invalid 'bib' argument used. Must be pymarc.Record instance."
        )

    if not isinstance(tag, str):
        raise CallNoConstructorError("Invalid 'tag' argument used. Must be string.")

    return bib[tag]


def get_language_code(bib: Record = None) -> Optional[str]:
    """
    Determines world lanugage code based on pos 35-37 of the 008 tag

    Args:
        bib:                pymarc.Record instance

    Returns:
        3-letter language code
    """
    if bib is None:
        return None

    try:
        code = bib["008"].data[35:38].lower()
        if code:
            return code
        else:
            return None
    except (AttributeError, IndexError):
        return None


def has_tag(bib: Record = None, tag: str = None) -> bool:
    """
    Checks if tag exists in record

    Args:
        bib:                pymarc.Record instance
        tag:                MARC tag as string

    Returns:
        boolean
    """
    if bib is None:
        return False
    elif not isinstance(tag, str):
        raise CallNoConstructorError("Invalid 'tag' argument used. Must be string.")

    return bool(bib[tag])


def is_short(bib: Record = None) -> Optional[bool]:
    """
    Determines if the print material is short
    """
    if bib is None:
        return None

    try:
        t300 = bib["300"]["a"]
    except TypeError:
        return None

    if t300 is None:
        return None

    short = False
    if "1 volume" in t300 or "1 v." in t300:
        short = True
    else:
        words = t300.split(" ")
        for w in words:
            try:
                if int(w) < 50:
                    short = True
            except ValueError:
                pass

    return short
