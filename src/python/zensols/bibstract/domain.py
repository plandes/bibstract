"""Domain and utility classes.

"""
__author__ = 'Paul Landes'

from typing import Set, Dict
from dataclasses import dataclass, field
import logging
from itertools import chain
from datetime import datetime
from io import TextIOWrapper
import re
import dateparser

logger = logging.getLogger(__name__)


@dataclass
class RegexFileParser(object):
    """Finds all instances of the citation references in a file.

    """
    REF_REGEX = re.compile(r'\{([a-zA-Z0-9,]+?)\}')
    """The default regular expression used to find citation references in sty and
    tex files (i.e. ``\\cite`` commands).

    """

    MULTI_REF_REGEX = re.compile(r'\s*,\s*')
    """The regular expression used to find comma separated lists of citations
    commands (i.e. ``\\cite``).

    """

    pattern: re.Pattern = field(default=REF_REGEX)
    """The regular expression pattern used to find the references."""

    collector: Set[str] = field(default_factory=lambda: set())
    """The set to add found references."""

    def find(self, fileobj: TextIOWrapper):
        for line in fileobj.readlines():
            refs = self.pattern.findall(line)
            refs = chain.from_iterable(
                map(lambda r: re.split(self.MULTI_REF_REGEX, r), refs))
            self.collector.update(refs)


@dataclass
class Converter(object):
    name: str = field()
    """The name of the converter, which is populated from the section name."""

    def convert(self, entry: Dict[str, str]) -> Dict[str, str]:
        return entry

    def __str__(self) -> str:
        return f'converter: {self.name}'


@dataclass
class DateToYearConverter(Converter):
    NAME = 'date_year'

    def convert(self, entry: Dict[str, str]) -> Dict[str, str]:
        if 'date' in entry:
            dt: datetime = dateparser.parse(entry['date'])
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"{entry['date']} -> {dt} -> {dt.year}")
            entry['year'] = str(dt.year)
        return entry
