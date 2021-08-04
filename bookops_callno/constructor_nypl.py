# -*- coding: utf-8 -*-

from pymarc import Record

from bookops_callno.base import CallNo


class NyplCallNo(CallNo):
    def __init__(self, bib: Record, requested_call_type: str):
        super().__init__(bib, requested_call_type)
