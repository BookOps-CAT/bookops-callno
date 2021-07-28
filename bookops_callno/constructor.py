# -*- coding: utf-8 -*-

"""
This module provides the main interface for the package
"""
from typing import Optional, Tuple

from pymarc import Record, Field

from bookops_callno.parser import (
    get_audience,
    get_field,
    get_form_of_item_code,
    get_language_code,
    get_main_entry_tag,
    get_physical_description,
    get_record_type_code,
)
from bookops_callno.errors import CallNoConstructorError


class CallNo:
    def __init__(self, bib: Record = None, requested_call_type: str = "auto"):
        """
        Call number constructor. The 'requested_call_type' may specify what type of
        the call number should be constructed (fiction, biography, etc.).
        The list below represents only same, shared between BPL & NYPL call number
        patterns and library specific call types that are possible
        (see documentation for specific library).

        Args:
            bib:                    pymarc.Record object
            requested_call_type:    type of call number to create; default 'auto';
                                    shared (BPL & NYPL) type patterns:
                                        - auto:             best match
                                        - fic:              fiction
                                        - bio:              biography
                                        - ebook:            ebook
                                        - dewey:            non-fic with Dewey
                                        - dewey-subject:    Dewey + subject pattern
                                        - movie:            DVD movie
                                        - tv:               DVD tv
        """
        if not isinstance(requested_call_type, str):
            raise CallNoConstructorError(
                "Invalid type of 'requested_call_type' argument used. Must be a string."
            )

        self.audience_info = None
        self.content_info = None
        self.cutter_info = None
        self.form_of_item_info = None
        self.language_info = None
        self.physical_desc_info = None
        self.record_type_info = None
        self.subject_info = None

        self.callno_field = None
        self.requested_call_type = requested_call_type

        self._prep(bib)

    def _prep(self, bib: Record) -> None:
        """
        Prepares elements for a call number creation
        """
        self.audience_info = self._get_audience_info(bib)
        self.cutter_info = self._get_main_entry_info(bib)
        self.form_of_item_info = self._get_form_of_item_info(bib)
        self.language_info = self._get_language_info(bib)
        self.physical_desc_info = self._get_physical_desciption(bib)
        self.record_type_info = self._get_record_type_info(bib)

    def _get_audience_info(self, bib: Record) -> Optional[str]:
        """
        Determines audience call number segment
        """
        audn = get_audience(bib)
        return audn

    def _get_form_of_item_info(self, bib: Record) -> Optional[str]:
        """
        Determines form of item MARC code
        """
        form_of_item = get_form_of_item_code(bib)
        return form_of_item

    def _get_language_info(self, bib: Record) -> Optional[str]:
        """
        Determines language code of the material
        """
        lang = get_language_code(bib)
        return lang

    def _get_main_entry_info(self, bib: Record) -> Tuple[str, Field]:
        """
        Determines 'main entry' of the bib.

        Returns namedTuple object with first element to be the entry and
        second elemet MARC tag it came from
        """
        tag = get_main_entry_tag(bib)
        field = get_field(bib, tag)

        return field

    def _get_physical_description_info(self, bib: Record) -> Optional[str]:
        """
        Returns MARC 300 tag value
        """
        physical_desc = get_physical_description(bib)
        return physical_desc

    def _get_record_type_info(self, bib: Record) -> Optional[str]:
        """
        Returns MARC leader record type code
        """
        rec_type = get_record_type(bib)
        return rec_type

    def as_pymarc_field(self) -> Field:
        """
        Returns constructed call number as `pymarc.Field` object
        """
        return self.callno_field

    def __repr__(self) -> str:
        """
        String representation of the constructed call number
        """
        if self.callno is not None:
            return self.callno_field.value()
        else:
            return ""


class BPLCallNo(CallNo):
    def __init__(self, bib: Record, requested_call_type: str):
        super().__init__(bib, requested_call_type)


class NYPLCallNo(CallNo):
    def __init__(self, bib: Record, requested_call_type: str):
        super().__init__(bib, requested_call_type)