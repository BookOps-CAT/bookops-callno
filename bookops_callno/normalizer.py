# -*- coding: utf-8 -*-

from typing import Optional

from pymarc import Field
from unidecode import unidecode, UnidecodeError


from bookops_callno.errors import CallNoConstructorError


def remove_trailing_punctuation(value: str) -> str:
    """
    Removes any trailing periods, commas, etc.

    Args:
        value:                  string to be processed

    Returns:
        value
    """
    if not isinstance(value, str):
        raise CallNoConstructorError(
            "Invalid 'value' type used in argument. Must be a string."
        )

    while value[-1] in ".,:;-() ":
        value = value[:-1]
    return value


def normalize_value(value: str) -> str:
    """
    Removes diacritics from string and changes to uppercase
    """
    if not value:
        return ""
    elif not isinstance(value, str):
        raise CallNoConstructorError(
            "Invalid 'value' type used in argument. Must be a string."
        )

    try:
        value = value.replace("\u02b9", "")  # Russian: modifier letter prime
        value = value.replace("\u02bb", "")  # Arabic modifier letter turned comma
        value = value.replace("'", "")
        value = unidecode(value, errors="strict")
        value = remove_trailing_punctuation(value).upper()
        return value
    except UnidecodeError as exc:
        raise CallNoConstructorError(
            f"Unsupported character encountered. Error: '{exc}'."
        )


def corporate_name_first_word(field: Field = None) -> Optional[str]:
    """
    Returns the uppdercase first word of the corporate entity from
    the 110 MARC tag

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "110":
        return None

    words = field["a"].strip().split(" ")
    name = normalize_value(words[0])
    return name


def corporate_name_full(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase full name of corporate entity.
    Uses the 110 MARC tag

    Args:
        field:                  pymarc.Field instance


    Returns:
        name
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag not in ("110", "610"):
        return None

    phrases = field["a"].strip().split("(")
    name = normalize_value(phrases[0])
    return name


def corporate_name_initial(field: Field = None) -> Optional[str]:
    """
    Returns the uppercase first letter of the corporate entity
    based on the 110 MARC tag

    Args:
        field:                  pymarc.Field instance

    Returns:
        initial
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "110":
        return None

    name = field["a"]
    name = normalize_value(name)
    initial = name[0]
    return initial


def personal_name_initial(field: Field = None) -> Optional[str]:
    """
    Returns the first letter of the last name of a personal author

    Args:
        field:                  pymarc.Field instance

    Returns
        initial
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "100":
        return None

    name = field["a"].strip()
    name = normalize_value(name)
    initial = name[0]
    return initial


def personal_name_surname(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase surname of personal author. Includes any numeration from
    the subield $b of 100 or 600 MARC tag.

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag not in ("100", "600"):
        return None
    elif field.indicator1 not in ("0", "1"):
        return None

    sub_a = field["a"].strip()

    # include subfield $b if present
    try:
        sub_b = field["b"].strip()
        name = f"{sub_a} {sub_b}"
    except AttributeError:
        name = sub_a

    name = normalize_value(name)

    # stop at comma to select surname
    try:
        stop = name.index(",")
        name = name[:stop]
    except ValueError:
        pass

    return name


def subject_corporate_name(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase corporate name to be used in subject segment
    of the call number based on MARC tag 610

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "610":
        return None

    name = corporate_name_full(field)
    return name


def subject_family_name(field: Field = None) -> Optional[str]:
    """
    Returns an uppercase family name based on the 600 MARC tag

    Args:
        field:                  pymarc.Field instance

    Returns:
        name
    """
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "600":
        return None
    elif field.indicator1 != "3":
        return None

    try:
        stop = field["a"].index("family")
        name = field["a"][:stop]
    except ValueError:
        return None

    name = normalize_value(name)
    return name


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
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "600":
        return None

    name = personal_name_surname(field)
    return name


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
    if field is None:
        return None
    elif not isinstance(field, Field):
        raise CallNoConstructorError(
            "Invalid 'field' argument type. Must be pymarc.Field instance."
        )

    if field.tag != "245":
        return None

    try:
        ind2 = int(field.indicator2)
    except ValueError:
        return None

    title = field["a"][ind2:]
    title = normalize_value(title)
    initial = title[0]
    return initial
