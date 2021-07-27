# -*- coding: utf-8 -*-

"""
This module provides the main interface for the package
"""
from collections import namedtuple
from typing import Optional, Tuple

from pymarc import Record, Field

from bookops_callno.parser import (
    get_field,
    get_main_entry_tag,
    get_audience,
    get_language_code,
)
from bookops_callno.errors import CallNoConstructorError


MainEntry = namedtuple("MainEntry", ["field", "tag"])


class CallNo:
    def __init__(
        self, bib: Record = None, library: str = None, requested_call_type: str = "auto"
    ):
        """
        Call number constructor. The 'library' argument specifies rules the call number
        should be using. The 'requested_call_type' may specify what type of
        the call number should be constructed (fiction, biography, etc.).
        The list below represents only same, shared between BPL & NYPL call number
        patterns and library specific call types that are possible
        (see documentation for specific library).

        Args:
            bib:                    pymarc.Record object
            library:                destination library
            requested_call_type:              type of call number to create; default 'auto';
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
        if not isinstance(library, str):
            raise CallNoConstructorError(
                "Invalid type of 'library' argument used. Must be a string."
            )

        if library.lower() not in ("bpl", "nyp", "nypl"):
            raise CallNoConstructorError(
                "Invalid 'library' value. Use 'bpl' or 'nypl'."
            )

        if not isinstance(requested_call_type, str):
            raise CallNoConstructorError(
                "Invalid type of 'requested_call_type' argument used. Must be a string."
            )

        self.library = library
        self.call_type_requested = requested_call_type
        self.call_type_produced = None
        self.segment_audn = None
        self.segment_content = None
        self.segment_cutter = None
        self.segment_format = None
        self.segment_language = None
        self.segment_subject = None

        self._prepare(bib)

    def _prepare(self, bib: Record) -> None:
        """
        Prepares elements for a call number creation
        """
        self.segment_audn = self._get_segment_audn(bib)
        self.segment_cutter = self._get_main_entry(bib)
        self.segment_language = self._get_segment_language(bib)

    def _get_segment_audn(self, bib: Record) -> Optional[str]:
        """
        Determines audience call number segment
        """
        audn = get_audience(bib)
        return audn

    def _get_segment_language(self, bib: Record) -> Optional[str]:
        """
        Determines language code of the material
        """
        lang = get_language_code(bib)
        return lang

    def _get_segment_format(self, bib: Record) -> Optional[str]:
        """
        Determines format of the material
        """
        pass

    def _get_main_entry(self, bib: Record) -> Tuple[str, Field]:
        """
        Determines 'main entry' of the bib.

        Returns namedTuple object with first element to be the entry and
        second elemet MARC tag it came from
        """
        tag = get_main_entry_tag(bib)
        field = get_field(bib, tag)

        return field

    def create(self):
        """
        Creates call number based on parsed previously data
        """
        pass

    def as_pymarc_field(self) -> Field:
        """
        Returns constructed call number as `pymarc.Field` object
        """
        return self.callno_field

    # def as_string(self) -> str:
    #     """
    #     Returns constructed call number as string
    #     """
    #     return self.callno_field.value()

    def __repr__(self) -> str:
        """
        String representation of the constructed call number
        """
        if self.callno is not None:
            return self.callno_field.value()
        else:
            return ""
