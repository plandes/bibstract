"""A library of built in converters.

"""
__author__ = 'Paul Landes'

from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import re
import dateparser
from zensols.config import ConfigFactory
from zensols.persist import persisted
from . import BibstractError, Converter, ConverterLibrary, DestructiveConverter

logger = logging.getLogger(__name__)


@dataclass
class DateToYearConverter(DestructiveConverter):
    """Converts the year part of a date field to a year.  This is useful when using
    Zotero's Better Biblatex extension that produces BibLatex formats, but you
    need BibTex entries.

    """
    NAME = 'date_year'
    """The name of the converter."""

    def _convert(self, entry: Dict[str, str]):
        if 'date' in entry:
            dt_str = entry['date']
            dt: datetime = dateparser.parse(dt_str)
            if dt is None:
                raise BibstractError(
                    f"Could not parse date: {dt_str} for entry {entry['ID']}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"{entry['date']} -> {dt} -> {dt.year}")
            entry['year'] = str(dt.year)
            if self.destructive:
                del entry['date']


@dataclass
class CopyOrMoveKeyConverter(DestructiveConverter):
    """Copy or move one or more fields in the entry.  This is useful when your
    bibliography style expects one key, but the output (i.e.BibLatex) outputs a
    different named field).

    When :obj:``destructive`` is set to ``True``, this copy operation becomes a
    move.

    """
    NAME = 'copy'
    """The name of the converter."""

    fields: Dict[str, str] = field(default_factory=dict)
    """The source to target list of fields specifying which keys to keys get copied
    or moved.

    """
    def _convert(self, entry: Dict[str, str]):
        for src, dst in self.fields.items():
            if src in entry:
                entry[dst] = entry[src]
                if self.destructive:
                    del entry[src]


@dataclass
class UpdateOrAddValue(Converter):
    """Update (clobber) or add a new mapping in an entry.

    """
    NAME = 'update'

    fields: List[Tuple[str, str]] = field(default_factory=list)
    """A list of tuples, each tuple having the key to add and the value to update
    or add using Python interpolation syntax from existing entry keys.

    """
    def _convert(self, entry: Dict[str, str]):
        for src, dst in self.fields:
            if src is None:
                src = 'ENTRYTYPE'
            try:
                val = dst.format(**entry)
            except KeyError as e:
                msg = f'Can not execute update/add converter for {entry["ID"]}'
                raise BibstractError(msg) from e
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'{src} -> {val}')
            entry[src] = val


@dataclass
class ConditionalConverter(Converter):
    """A converter that invokes a list of other converters if a certain entry
    key/value pair matches.

    """
    config_factory: ConfigFactory = field()
    """The configuration factory used to create this converter and used to get
    referenced converters.

    """

    converters: List[str] = field(default_factory=list)
    """The list of converters to inovke if the predicate condition is satisfied.

    """

    includes: Dict[str, str] = field(default_factory=dict)
    """The key/values that must match in the entry to invoke the converters
    referenced by :obj:`converters`.

    """

    excludes: Dict[str, str] = field(default_factory=dict)
    """The key/values that can *not* match in the entry to invoke the converters
    referenced by :obj:`converters`.

    """
    @persisted('_converter_insts')
    def _get_converters(self):
        lib: ConverterLibrary = self.config_factory('converter_library')
        return tuple(map(lambda n: lib[n], self.converters))

    def _matches(self, entry: Dict[str, str], crit: Dict[str, str],
                 negate: bool) -> bool:
        matches = True
        for k, v in crit.items():
            val = entry.get(k)
            if val is None:
                if negate:
                    matches = False
                    break
            else:
                is_match = re.match(v, val)
                if negate:
                    is_match = not is_match
                if is_match:
                    matches = False
                    break
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'matches: {matches}: {crit} ' +
                         f'{"!=" if negate else "=="} {entry}')
        return matches

    def _convert(self, entry: Dict[str, str]):
        # matches = True
        
        # for k, v in self.includes.items():
        #     if entry.get(k) != v:
        #         matches = False
        #         break
        # if matches:
        #     for k, v in self.excludes.items():
        #         if entry.get(k) == v:
        #             matches = False
        #             break
        if self._matches(entry, self.includes, True) and \
           self._matches(entry, self.excludes, False):
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'matches on {entry["ID"]}: {self.includes}')
            for conv in self._get_converters():
                entry.update(conv.convert(entry))
