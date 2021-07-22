# -*- coding: utf-8 -*-

"""
This module provides the main interface for the package
"""

from pymarc import Record, Field


class CallNo:
    def __init__(self, bib_obj: Record, library: str, call_type: str = "auto"):
        """
        Call number constructor. The 'library' argument specifies rules the call number
        should be using. The 'call_type' may specify what type of the call number
        should be constructed (fiction, biography, etc.). The list below represents
        only same, shared between BPL & NYPL call number patterns and library
        specific call_types are possible (see documentation for specific library).

        Args:
            bib_obj:                pymarc.Record object
            library:                destination library
            call_type:              type of call number to create; default 'auto';
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
        self.bib = bib_obj
        self.library = library
        self.call_type = call_type

    def as_marc(self) -> Field:
        """
        Returns constructed call number as `pymarc.Field` object
        """
        pass

    def __repr__(self):
        """
        String representation of the constructed call number
        """
        pass
