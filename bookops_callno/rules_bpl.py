# -*- coding: utf-8 -*-

from typing import Optional

from bookops_callno.parser import is_libretto


def callno_format_prefix(
    record_type_code: str = None, form_of_item: str = None
) -> Optional[str]:
    """
    Args:
        record_type_code:               MARC leader position 6
        form_of_item:                   MARC tag 008 form of item

    Returns:
        format_prefix
    """
    if record_type_code in ("a", "t"):
        if form_of_item in ("o", "s"):
            return "eBOOK"
        elif form_of_item in ("a", "b"):
            return "NM"
        elif is_libretto():
            return "LIB"
        else:
            return None
    elif record_type_code in ("c", "d"):
        return "Mu"

    # nonmusical sound recordings
    elif record_type_code == "i":
        if form_of_item in ("o", "s"):
            return "eAUDIO"
        else:
            return "AUDIO"
    elif record_type_code == "j":
        if form_of_item in ("o", "s"):
            return "eMUSIC"
        else:
            return "CD"

    # visual materials
    elif record_type_code == "g":
        if form_of_item in ("o", "s"):
            return "eVIDEO"
        else:
            return "DVD"
