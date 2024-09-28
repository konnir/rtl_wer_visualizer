import logging
import os
import re
from typing import List, Dict, Any
from fastapi import UploadFile
from jiwer import process_words, WordOutput


class AllowedReplacementsHandler:

    def __init__(self) -> None:
        self.__allowed_replacements = self._read_allowed_replacements()

    def apply_allowed_replacements(self, txt: str) -> str:
        txt_clean = txt
        if self.__allowed_replacements:
            txt_clean, _ = self._replace_whole_words(txt)
        return txt_clean

    def _replace_whole_words(self, text: str) -> tuple[str, int]:
        replaces = 0
        for rep, lace in self.__allowed_replacements.items():
            pattern = re.compile(r'\b' + re.escape(rep) + r'\b')
            if pattern.search(text):
                text = pattern.sub(lace, text)
                replaces += 1
        return text, replaces

    def _read_allowed_replacements(self) -> dict[str, str]:
        allowed_replacements_path = os.getenv(
            key="ALLOWED_REPLACEMENTS_PATH",
            default="service/custom/allowed_replacements.txt",
        )
        with open(allowed_replacements_path, "r") as f:
            allowed_replacements = f.read()
        allowed_replacements_dict = self._parse_replacements(allowed_replacements)
        allowed_replacements_sorted = dict(
            sorted(
                allowed_replacements_dict.items(),
                key=lambda item: len(item[0].split()),
                reverse=True,
            )
        )
        return allowed_replacements_sorted

    def _parse_replacements(self, replacements: str) -> dict:
        replacements_dict = {}
        for line in replacements.split("\n"):
            parts = [part.strip() for part in line.split(",")]
            if len(parts) == 2:
                key, value = parts
                replacements_dict[key] = value
        return replacements_dict
