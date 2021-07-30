# -*- coding: utf-8 -*-

from typing import Optional

from pymarc import Field


def corporate_name_first_word(field: Field = None) -> Optional[str]:
    """
    Returns the uppdercase first word of the corporate entity from
    the 110 MARC tag

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    pass


def corporate_name_full(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase full name of corporate entity.
    Uses the 110 MARC tag

    Args:
        field:                  pymarc.Field instance


    Returns:
        name
    """
    pass


def corporate_name_initial(field: Field = None) -> Optional[str]:
    """
    Returns the uppercase first letter of the corporate entity
    based on the 110 MARC tag

    Args:
        field:                  pymarc.Field instance

    Returns:
        initial
    """
    pass


def personal_name_initial(field: Field = None) -> Optional[str]:
    """
    Returns the first letter of the last name of a personal author

    Args:
        field:                  pymarc.Field instance

    Returns
        initial
    """
    pass


def personal_name_surname(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase surname of personal author

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    pass


def subject_corporate_name(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase corporate name to be used in subject segment
    of the call number based on MARC tag 610

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    pass


def subject_personal_name(field: Field = None) -> Optional[str]:
    """
    Returns personal name to be used in subject segment of the call
    number. Use for biography or Dewey + Name patters, examples:
        biography: B LOUIS XIV C
        criticizm of works of an author: 813 ADAMS C

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    pass


def subject_topic(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase topic to be used in the subject segment of the call
    number based on MARC tag 650. Valid only for BPL call numbers.
    Examples: programming language, name of operating system, etc.

    Args:
        field:                  pymarc.Field instance

    Returns:
        topic
    """
    pass


def title_first_word(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase first word (skipping any articles) of
    the title field (245 MARC tag subfield $a).

    Args:
        field:                  pymarc.Field instance

    Returns:
        word
    """
    pass


def title_initial(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase initial (skipping any articles) of
    the title field (245 MARC tag subfield $a).

    Args:
        field:                  pymarc.Field instance

    Returns:
        initial
    """
    pass
