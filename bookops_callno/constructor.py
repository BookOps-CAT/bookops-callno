# -*- coding: utf-8 -*-

"""
This module provides the main interface for the package
"""
from typing import Optional, Tuple

from pymarc import Record, Field

from bookops_callno.parser import (
    get_audience,
    get_callno_relevant_subjects,
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
        Genaral call number constructor. The 'requested_call_type' may specify what type of
        the call number should be constructed (fiction, biography, etc.). See BPLCallNo
        and NYPLCallNo classes for the details.

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
        self.subject_info = []

        self.callno_field = None
        self.requested_call_type = requested_call_type

        self._prep(bib)

    def __repr__(self) -> str:
        """
        String representation of the constructed call number
        """
        if self.callno_field is not None:
            return self.callno_field.value()
        else:
            return ""

    def _prep(self, bib: Record) -> None:
        """
        Prepares elements for a call number creation
        """
        self.audience_info = self._get_audience_info(bib)
        self.cutter_info = self._get_main_entry_info(bib)
        self.form_of_item_info = self._get_form_of_item_info(bib)
        self.language_info = self._get_language_info(bib)
        self.physical_desc_info = self._get_physical_description_info(bib)
        self.record_type_info = self._get_record_type_info(bib)
        self.subject_info = self._get_subject_info(bib)

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
        rec_type = get_record_type_code(bib)
        return rec_type

    def _get_subject_info(self, bib: Record) -> Optional[str]:
        """
        Returns list of relevant for call number creation 6xx tags
        """
        subjects = get_callno_relevant_subjects(bib)
        return subjects

    def as_pymarc_field(self) -> Optional[Field]:
        """
        Returns constructed call number as `pymarc.Field` object
        """
        return self.callno_field


class BplCallNo(CallNo):
    def __init__(
        self,
        bib: Record = None,
        requested_call_type: str = "auto",
        strict_mode: bool = True,
    ):
        super().__init__(bib, requested_call_type)

        self.tag = "099"
        self.inds = [" ", " "]
        self.strict_mode = strict_mode

        self._create()

    def _create(self):
        """
        Creates call number
        """
        if self.requested_call_type == "eaudio":
            self.callno_field = Field(
                tag=self.tag,
                indicators=self.inds,
                subfields=["a", "eAUDIO"],
            )
        elif self.requested_call_type == "ebook":
            self.callno_field = Field(
                tag=self.tag, indicators=self.inds, subfields=["a", "eBOOK"]
            )
        elif self.requested_call_type == "evideo":
            self.callno_field = Field(
                tag=self.tag, indicators=self.inds, subfields=["a", "eVIDEO"]
            )


class NyplCallNo(CallNo):
    def __init__(self, bib: Record, requested_call_type: str):
        super().__init__(bib, requested_call_type)
