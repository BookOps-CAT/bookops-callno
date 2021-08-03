# -*- coding: utf-8 -*-

"""
This module provides the main interface for the package
"""
from typing import List, Optional, Tuple

from pymarc import Record, Field


from bookops_callno.errors import CallNoConstructorError
from bookops_callno.normalizer import (
    corporate_name_initial,
    personal_name_surname,
    title_initial,
)
from bookops_callno.parser import (
    get_audience,
    get_callno_relevant_subjects,
    get_field,
    get_form_of_item_code,
    get_language_code,
    get_main_entry_tag,
    get_physical_description,
    get_record_type_code,
    is_biography,
    is_dewey,
    is_dewey_plus_subject,
    is_fiction,
)


class CallNo:
    def __init__(self, bib: Record = None, requested_call_type: str = "auto"):
        """
        Genaral call number constructor. The 'requested_call_type' may specify what
        type of the call number should be constructed (fiction, biography, etc.).
        See BPLCallNo and NYPLCallNo classes for the details.

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
        self.content_info = self._get_content_info(bib)

    def _get_audience_info(self, bib: Record) -> Optional[str]:
        """
        Determines audience call number segment
        """
        audn = get_audience(bib)
        return audn

    def _get_content_info(self, bib: Record) -> str:
        """
        Determines broad material content

        Returns:
            content:            options:
                                    - pic (picture book)
                                    - fic (fiction)
                                    - dew (dewey)
                                    - bio (biography)
                                    - des (dewey + subject)
                                    - und (undetermined)
        """
        # print material
        if self.record_type_info in ("a", "t"):
            # order matters!
            if self.audience_info == "early juv":
                self.content_info = "pic"
            elif is_fiction(bib):
                self.content_info = "fic"
            elif is_dewey_plus_subject(bib):
                self.content_info = "des"
            elif is_biography(bib):
                self.content_info = "bio"
            elif is_dewey(bib):
                self.content_info = "dew"
            else:
                self.content_info = "und"
        # visual material
        elif self.record_type_info == "g":
            pass

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
        Determines a 'main entry' field of the bib.
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

        self.mat_format = self._get_material_format()
        self._create()

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

    def _create_eaudio_callno(self):
        """
        Creates call number for electronic audiobook (eAUDIO)
        """
        return Field(
            tag=self.tag,
            indicators=self.inds,
            subfields=["a", "eAUDIO"],
        )

    def _create_ebook_callno(self):
        """
        Creates call number field for ebook (eBOOK)
        """
        return Field(tag=self.tag, indicators=self.inds, subfields=["a", "eBOOK"])

    def _create_evideo_callno(self):
        """
        Creates call number field for evideo (eVideo)
        """
        return Field(tag=self.tag, indicators=self.inds, subfields=["a", "eVIDEO"])

    def _create_fic_callno(self) -> Optional[str]:
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

        # determine language
        if self.language_info is not None and self.language_info != "eng":
            lang = self.language_info.upper()
        else:
            lang = None

        # determine audience
        if self.audience_info == "juv":
            audn = "J"
        else:
            audn = None

        # determine cutter
        main_entry_tag = self.cutter_info.tag
        if main_entry_tag == "100":
            cutter = personal_name_surname(field=self.cutter_info)
        elif main_entry_tag == "110":
            cutter = corporate_name_initial(field=self.cutter_info)
        elif main_entry_tag == "245":
            cutter = title_initial(field=self.cutter_info)
        else:
            cutter = None

        if not cutter:
            return None
        else:
            elements = [e for e in [form, lang, audn, "FIC", cutter] if e]
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

    def _get_material_format(self):
        """
        Determines material format
        """
        pass


class NyplCallNo(CallNo):
    def __init__(self, bib: Record, requested_call_type: str):
        super().__init__(bib, requested_call_type)
