from pathlib import Path
from enum import Enum, auto
import re


def update_basepath(old_basepath: Path | None, new_basepath: Path | None, path: Path) -> Path:
    """
    Update a single file path that is relative to a base path that has changed.

    If the path is absolute, it is returned unchanged.
    If it is relative, it is updated to be relative to the new base path, unless that base path is not an
    ancestor of the old full path, in which case the absolute path is returned.
    """
    if old_basepath is None and not path.is_absolute():
        # If the old base path is not known, we can't reliably update the relative path, so we return it unchanged.
        return path
    old_full_path = path if old_basepath is None else (old_basepath / path).resolve()
    if new_basepath is None:
        # If the new base path is not known, we can't reliably update the relative path, so we return the absolute path.
        return old_full_path
    try:
        # We don't walk up. If this fails, we'll just use the absolute path
        return old_full_path.relative_to(new_basepath)
    except ValueError:
        return old_full_path


# The following case functions are adapted from:
# https://github.com/Virtlink/pidgyn/blob/d2e057f9b3a03c8b1f5a1f9330740ea5aa9cb1be/pidgyn-utils/src/main/kotlin/net/pelsmaeker/pidgyn/text/CharSequence.ext.kt#L137-L311


class SentenceCase(Enum):
    UPPER_CAMEL = auto()
    LOWER_CAMEL = auto()
    UPPER_UNDERSCORE = auto()
    LOWER_UNDERSCORE = auto()
    UPPER_HYPHEN = auto()
    LOWER_HYPHEN = auto()
    SPACE = auto()


class WordCase(Enum):
    UPPER = auto()
    LOWER = auto()
    CAPITALIZED = auto()


def format_word_as(word: str, fmt: WordCase) -> str:
    if fmt is WordCase.UPPER:
        return word.upper()
    if fmt is WordCase.LOWER:
        return word.lower()
    # CAPITALIZED
    if not word:
        return word
    first = word[0].upper() if word[0].islower() else word[0]
    rest = word[1:].lower()
    return first + rest


def split_to_words(s: str, fmt: SentenceCase | None = None) -> list[str]:
    if s == "":
        return []

    if fmt in (SentenceCase.UPPER_CAMEL, SentenceCase.LOWER_CAMEL):
        words: list[str] = []
        current: list[str] = []
        length = len(s)
        for i, c in enumerate(s):
            # Boundary if previous char was not upper OR next char is not upper
            if c.isupper() and current and (
                (i > 0 and not s[i - 1].isupper()) or (i < length - 1 and not s[i + 1].isupper())
            ):
                words.append("".join(current))
                current = []
            current.append(c)
        if current:
            words.append("".join(current))
        return words

    if fmt in (SentenceCase.UPPER_UNDERSCORE, SentenceCase.LOWER_UNDERSCORE):
        parts = s.split("_")
        return [p for p in parts if p]

    if fmt in (SentenceCase.UPPER_HYPHEN, SentenceCase.LOWER_HYPHEN):
        parts = s.split("-")
        return [p for p in parts if p]

    if fmt is SentenceCase.SPACE:
        parts = s.split(" ")
        return [p for p in parts if p]

    intermediate = re.split(r"[_\-\s]+", s)
    result: list[str] = []
    for part in intermediate:
        if part:
            result.extend(split_to_words(part, SentenceCase.UPPER_CAMEL))
    return result


def join_to_case_format(words: list[str], fmt: SentenceCase) -> str:
    if fmt is SentenceCase.UPPER_CAMEL:
        return "".join(format_word_as(w, WordCase.CAPITALIZED) for w in words)

    if fmt is SentenceCase.LOWER_CAMEL:
        if not words:
            return ""
        first = format_word_as(words[0], WordCase.LOWER)
        rest = "".join(format_word_as(w, WordCase.CAPITALIZED) for w in words[1:])
        return first + rest

    if fmt is SentenceCase.UPPER_UNDERSCORE:
        return "_".join(format_word_as(w, WordCase.UPPER) for w in words)

    if fmt is SentenceCase.LOWER_UNDERSCORE:
        return "_".join(format_word_as(w, WordCase.LOWER) for w in words)

    if fmt is SentenceCase.UPPER_HYPHEN:
        return "-".join(format_word_as(w, WordCase.UPPER) for w in words)

    if fmt is SentenceCase.LOWER_HYPHEN:
        return "-".join(format_word_as(w, WordCase.LOWER) for w in words)

    # SPACE
    return " ".join(words)


# Convenience converters
def to_lower_camel_case(s: str) -> str:
    return join_to_case_format(split_to_words(s), SentenceCase.LOWER_CAMEL)


def to_upper_camel_case(s: str) -> str:
    return join_to_case_format(split_to_words(s), SentenceCase.UPPER_CAMEL)


def to_lower_underscore_case(s: str) -> str:
    return join_to_case_format(split_to_words(s), SentenceCase.LOWER_UNDERSCORE)


def to_upper_underscore_case(s: str) -> str:
    return join_to_case_format(split_to_words(s), SentenceCase.UPPER_UNDERSCORE)


def to_lower_hyphen_case(s: str) -> str:
    return join_to_case_format(split_to_words(s), SentenceCase.LOWER_HYPHEN)


def to_upper_hyphen_case(s: str) -> str:
    return join_to_case_format(split_to_words(s), SentenceCase.UPPER_HYPHEN)
