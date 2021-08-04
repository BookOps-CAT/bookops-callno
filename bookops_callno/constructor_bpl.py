# -*- coding: utf-8 -*-

from typing import List, Optional

from pymarc import Record, Field

from bookops_callno.base import CallNo
from bookops_callno.normalizer import (
    corporate_name_first_word,
    corporate_name_initial,
    personal_name_surname,
    title_initial,
)
from bookops_callno.rules_bpl import callno_format_prefix
from bookops_callno.rules_shared import (
    callno_cutter_fic,
    callno_cutter_initial,
    callno_cutter_pic,
)


class BplCallNo(CallNo):
    def __init__(
        self,
        bib: Record = None,
        order_audn: str = None,
        order_lang: str = None,
        order_note: str = None,
        order_shelf: str = None,
        requested_call_type: str = "auto",
    ):
        """
        Args:

            bib:                    pymarc.Record instance
            order_audn:             order audience
            order_lang:             order language
            order_note:             vendor note/po per line
            order_shelf:            order shelf code
            requested_call_type:    call pattern to be created;
                                    options:
                                        - auto
                                        - eaudio
                                        - ebook
                                        - evideo
                                        - fic
        """
        super().__init__(bib, requested_call_type)

        self.tag = "099"
        self.inds = [" ", " "]
        self.order_audn = order_audn
        self.order_lang = order_lang
        self.order_note = order_note
        self.order_shelf = order_shelf

        self.mat_format = callno_format_prefix()
        self._create()

    def _cleanup_callno_elements(self, elements: List) -> List:
        """
        Removes from a list elements that have value None
        """
        return [e for e in elements if e]

    def _create(self):
        """
        Creates call number
        """
        if self.requested_call_type == "eaudio":
            self.callno_field = self._create_eaudio_callno()
        elif self.requested_call_type == "ebook":
            self.callno_field = self._create_ebook_callno()
        elif self.requested_call_type == "evideo":
            self.callno_field = self._create_evideo_callno()
        elif self.requested_call_type == "fic":
            self.callno_field = self._create_fic_callno()
        elif self.requested_call_type == "pic":
            self.callno_field = self._create_pic_callno()
        elif self.requested_call_type == "bio":
            self.callno_field = self._create_bio_callno()

    def _create_eaudio_callno(self) -> Optional[Field]:
        """
        Creates call number for electronic audiobook (eAUDIO)
        """
        return Field(
            tag=self.tag,
            indicators=self.inds,
            subfields=["a", "eAUDIO"],
        )

    def _create_ebook_callno(self) -> Optional[Field]:
        """
        Creates call number field for ebook (eBOOK)
        """
        return Field(tag=self.tag, indicators=self.inds, subfields=["a", "eBOOK"])

    def _create_evideo_callno(self) -> Optional[Field]:
        """
        Creates call number field for evideo (eVideo)
        """
        return Field(tag=self.tag, indicators=self.inds, subfields=["a", "eVIDEO"])

    def _create_fic_callno(self) -> Optional[Field]:
        """
        Creates call number field for fiction, patterns:
            FIC ADAMS
            FIC T
            J FIC ADAMS
            SPA FIC ADAMS
            SPA J FIC ADAMS
            AUDIO FIC ADAMS
            AUDIO SPA J FIC ADAMS
        """
        # determine material format
        if self.mat_format == "audio":
            form = "AUDIO"
        else:
            form = None

        # determine audience
        if self.audience_info == "juv":
            audn = "J"
        else:
            audn = None

        # determine cutter
        cutter = callno_cutter_fic(self.cutter_info)

        if not cutter:
            return None
        else:
            elements = [form, self.language_code, audn, "FIC", cutter]
            elements = self._cleanup_callno_elements(elements)
            subfields = self._construct_subfields(elements)
            return Field(tag=self.tag, indicators=self.inds, subfields=subfields)

    def _create_pic_callno(self) -> Optional[Field]:
        """
        Creates call number field for picture books and early readers.
        Patterns:
            J-E ADAMS
            J-E A
            CHI J-E ADAMS
        """
        cutter = callno_cutter_pic(self.cutter_info)
        if not cutter:
            return None
        else:
            elements = [e for e in [self.language_code, "J-E", cutter] if e]
            subfields = self._construct_subfields(elements)
            return Field(tag=self.tag, indicators=self.inds, subfields=subfields)

    def _create_dew_callno(self) -> Optional[Field]:
        """
        Creates call number field for nonfiction materials classed in Dewey

        Patterns:
            811 A
            947.08 B
            J 741.23 T
            POL 821 A
            CHI J 500 D
            AUDIO 348.2367 D
            AUDIO SPA J 811 D
            DVD 909.0492 M
            BOOK & CD 323.623 W
        """
        pass

    def _create_bio_callno(self) -> Optional[Field]:
        """
        Creates call number field for biography and autobiography

        Patterns:
            B ADAMS G
            CHI B ADAMS G
            AUDIO B ADAMS G
            AUDIO CHI B ADAMS G
            DVD B ADAMS G
            DVD CHI B ADAMS G
            BOOK & CD B ADAMS G
        """
        # determine audience
        if self.audience_info == "juv":
            audn = "J"
        else:
            audn = None

        # determine biographee segment
        biographee = None
        for field in self.subject_info:
            if field.tag == "600":
                biographee = subject_personal_name(filed)
                break  # select first encountered field
        if biographee is None:
            return None

        # determine cutter
        cutter = callno_cutter_initial(self.cutter_info)
        if not cutter:
            return None
        else:
            elements = [
                e
                for e in [
                    self.mat_format,
                    self.language_code,
                    audn,
                    "B",
                    biographee,
                    cutter,
                ]
                if e
            ]
            subfields = self._construct_subfields(elements)
            return Field(tag=self.tag, indicators=self.inds, subfields=subfields)

    def _construct_subfields(self, elements: List[str]) -> List:
        """
        Constructs properly formatted list of subfields by inserting subfield $a
        before each element

        Args:
            elements:               list of call number elements in order they
                                    should appear on the bib
        """
        subfields = []
        for e in elements:
            subfields.extend(["a", e])
        return subfields
