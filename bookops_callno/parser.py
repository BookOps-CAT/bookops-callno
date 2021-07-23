# -*- coding: utf-8 -*-

"""
This module contains methods to parse MARC records in a form of pymarc.Record objects
"""

from typing import Optional

from pymarc import Record, Field


from bookops_callno.errors import CallNoConstructorError


def has_tag(bib: Record = None, tag: str = None) -> bool:
    """
    Checks if tag exists in record

    Args:
        bib:                pymarc.Record instance
        tag:                MARC tag as string

    Returns:
        boolean
    """
    if not isinstance(bib, Record):
        raise CallNoConstructorError(
            "Invalid 'bib' argument used. Must be pymarc.Record instance."
        )

    if not isinstance(tag, str):
        raise CallNoConstructorError("Invalid 'tag' argument used. Must be string.")

    return bool(bib[tag])


def main_entry_tag(bib: Record = None) -> Optional[str]:
    """
    Determines MARC tag of the main entry

    Args:
        bib:                    pymarc.Record instance

    Returns:
        tag
    """
    if not isinstance(bib, Record):
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
    if not isinstance(bib, Record):
        raise CallNoConstructorError(
            "Invalid 'bib' argument used. Must be pymarc.Record instance."
        )

    if not isinstance(tag, str):
        raise CallNoConstructorError("Invalid 'tag' argument used. Must be string.")

    return bib[tag]
