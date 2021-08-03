# -*- coding: utf-8 -*-

"""
This module contains methods to parse MARC records in a form of pymarc.Record objects
"""

from typing import List, Optional

from pymarc import Record, Field


from bookops_callno.errors import CallNoConstructorError


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


def get_callno_relevant_subjects(bib: Record = None) -> List[Field]:
    """
    Parses call number relevant subject MARc fields

    Args:
        bib:                    pymarc.Record instance

    Returns:
        subject_fields
    """
    if bib is None:
        return []
    elif not isinstance(bib, Record):
        raise CallNoConstructorError(
            "Invalid 'bib' argument used. Must be pymarc.Record instance."
        )

    subject_fields = []
    for field in bib.get_fields("600", "610"):
        if is_lc_subject(field):
            subject_fields.append(field)

    for field in bib.get_fields("650"):
        if is_lc_subject(field):
            subject_fields.append(field)

    return subject_fields


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


def get_form_of_item_code(bib: Record = None) -> Optional[str]:
    """
    Parses form of item code in the 008 tag if exists

    Args:
        bib:                    pymarc.Record instance

    Returns:
        code
    """
    if bib is None:
        return None
    elif not isinstance(bib, Record):
        raise CallNoConstructorError(
            "Invalid 'bib' argument used. Must be pymarc.Record instance."
        )
    rec_type = bib.leader[6]
    try:
        # print, sound records, computer files
        if rec_type in ("a", "c", "d", "i", "j", "m", "t"):
            return bib["008"].data[23]
        # visual materials
        elif rec_type == "g":
            return bib["008"].data[29]
        else:
            return None
    except (AttributeError, IndexError):
        return None


def get_format_bpl(bib: Record = None) -> Optional[str]:
    """
    Determines material format based on the leader and tag 008 of the
    MARC record

    Args:
        bib:                    pymarc.Record instance

    Returns:
        bib_format
    """
    pass


#     if bib is None:
#         return None
#     # elif not isinstance(bib, Record):
#     #     raise CallNoConstructorError(
#     #         "Invalid 'bib' argument used. Must be pymarc.Record instance."
#     #     )

#     rec_type = bib.leader[6]
#     bib_lvl = bib.leader[7]
#     item_form = get_form_of_item_code(bib)
#     t300 = bib["300"].value()


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


def get_physical_description(bib: Record = None) -> Optional[str]:
    """
    Returns value of MARC tag 300
    """
    if bib is None:
        return None

    try:
        t300 = bib["300"].value()
        return t300
    except AttributeError:
        return None


def get_record_type_code(bib: Record = None) -> Optional[str]:
    """
    Parses MARC leader for record type code

    Args:
        bib:                pymarc.Record instance

    Returns:
        rec_type_code
    """
    if bib is None:
        return None

    rec_type_code = bib.leader[6]
    return rec_type_code


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


def is_biography(bib: Record = None) -> bool:
    """
    Determines if material is autobiography or biography
    """
    if bib is None:
        return False

    rec_type = get_record_type_code(bib)
    if rec_type in (
        "a",
        "t",
    ):  # print material
        try:
            code = bib["008"].data[34]
        except AttributeError:
            return False

        if code in ("a", "b"):
            return True
        else:
            return False
    elif rec_type == "i":  # nonmusical sound recording
        code = bib["008"].data[30]
        if code in ("a", "b"):
            return True
        else:
            return False
    else:
        return False


def is_dewey(bib: Record = None) -> bool:
    """
    Determines if material can be classified using Dewey

    Args:
        bib:                pymarc.Record instance

    Returns:
        boolean
    """
    pass


def is_dewey_plus_subject(bib: Record = None) -> bool:
    """
    Determines if material can be classified using Dewey + subject pattern

    Args:
        bib:                pymarc.Record instance

    Returns:
        boolean
    """
    pass


def is_fiction(bib: Record = None) -> bool:
    """
    Determines if material is fiction

    Args:
        bib:                pymarc.Record instance

    Returns:
        boolean
    """
    pass


def is_lc_subject(field: Field = None) -> bool:
    """
    Determies if subject belongs to LCSH

    Args:
        field:              pymarc.Field instance

    Returns:
        boolean
    """

    if field is None:
        return False
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument. Must be an instance of 'pymarc.Field'."
        )

    if field.tag in ("600", "610", "611", "630", "650", "651", "655"):
        if field.indicator2 == "0":
            return True
        else:
            return False
    else:
        return False


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
