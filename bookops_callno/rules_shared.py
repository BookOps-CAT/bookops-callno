# -*- coding: utf-8 -*-

from typing import List, Optional

from pymarc import Field


from bookops_callno.normalizer import (
    corporate_name_first_word,
    corporate_name_initial,
    personal_name_surname,
    personal_name_initial,
    title_initial,
)


def biographee(subjects: List[Field]) -> Optional[str]:
    """
    Constructs biographee component of the call number.

    Args:
        subjects:                       list of pymarc.Field instances

    Returns:
        biographee
    """
    for field in subjects:
        if field.tag == "600":
            biographee = personal_name_surname(field)
            return biographee


def callno_cutter_fic(field: Field = None) -> Optional[str]:
    """
    Constructs cutter subfield for fiction call number patterns.

    Args:
        field:                          pymarc.Field instance

    Returns:
        cutter
    """
    if field is None or not isinstance(field, Field):
        return None

    if field.tag == "100":
        cutter = personal_name_surname(field)
    elif field.tag == "110":
        cutter = corporate_name_initial(field)
    elif field.tag == "245":
        cutter = title_initial(field)
    else:
        cutter = None
    return cutter


def callno_cutter_initial(field: Field = None) -> Optional[str]:
    """
    Constructs cutter constiting of the first letter of the main entry.

    Args:
        field:                          pymarc.Field instance

    Returns:
        cutter
    """
    if field is None or not isinstance(field, Field):
        return None

    if field.tag == "100":
        cutter = personal_name_initial(field)
    elif field.tag == "110":
        cutter = corporate_name_initial(field)
    elif field.tag == "245":
        cutter = title_initial(field)
    else:
        cutter = None

    return cutter


def callno_cutter_pic(field: Field = None) -> Optional[Field]:
    """
    Constructs cutter subfield for picture books and BPL's easy readers.

    Args:
        field:                          pymarc.Field instance

    Returns:
        cutter
    """
    if field is None or not isinstance(field, Field):
        return None

    if field.tag == "100":
        cutter = personal_name_surname(field)
    elif field.tag == "110":
        cutter = corporate_name_first_word(field)
    elif field.tag == "245":
        cutter = title_initial(field)
    else:
        cutter = None
    return cutter
