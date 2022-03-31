"""This utility extracts Bib(La)Tex references (a.k.a *markers*) from a
(La)Tex.

"""
__author__ = 'Paul Landes'

from typing import Dict
from dataclasses import dataclass, field
import logging
import os
from pathlib import Path
from zensols.config import ConfigFactory
from . import Extractor, ConverterLibrary

logger = logging.getLogger(__name__)


@dataclass
class Exporter(object):
    """This utility extracts Bib(La)Tex references from a (La)Tex.

    """
    CLI_META = {'mnemonic_excludes': {'get_extractor'},
                'mnemonic_overrides': {'print_bibtex_ids': 'showbib',
                                       'print_texfile_refs': 'showtex',
                                       'print_extracted_ids': 'showextract',
                                       'print_entry': 'entry'},
                'option_includes': {'output'},
                'option_overrides': {'output': {'long_name': 'output',
                                                'short_name': 'o'}}}

    config_factory: ConfigFactory = field()
    """The configuration factory used to create this instance."""

    converter_library: ConverterLibrary = field()
    """The converter library used to print what's available."""

    log_name: str = field()
    """The name of the package logger."""

    def get_extractor(self, texpath: Path = None) -> Extractor:
        return self.config_factory.new_instance('extractor', texpath=texpath)

    def _set_log_level_info(self):
        #logging.getLogger(self.log_name).setLevel(logging.INFO)
        pass

    def converters(self):
        """List converters and their information."""
        self.converter_library.write()

    def print_bibtex_ids(self):
        """Print BibTex citation keys."""
        extractor = self.get_extractor()
        extractor.print_bibtex_ids()

    def print_texfile_refs(self, texpath: Path):
        """Print citation references.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        """
        extractor = self.get_extractor(texpath)
        extractor.print_texfile_refs()

    def print_extracted_ids(self, texpath: Path):
        """Print BibTex export citation keys.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        """
        extractor = self.get_extractor(texpath)
        extractor.print_extracted_ids()

    def print_entry(self, citation_key: str):
        """Print a single BibTex entry as it would be given in the output.

        :param citation_key: the citation key of entry to print out

        """
        extractor = self.get_extractor()
        entry: Dict[str, Dict[str, str]] = extractor.get_entry(citation_key)
        extractor.write_entry(entry)

    def export(self, texpath: Path, output: Path = None):
        """Export the derived BibTex file.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        :param output: the output path name, or standard out if not given

        """
        self._set_log_level_info()
        extractor = self.get_extractor(texpath)
        if output is None:
            extractor.extract()
        else:
            with open(output, 'w') as f:
                extractor.extract(writer=f)

    def export_all(self, texpaths: str, output: Path = None):
        """Export the derived BibTex file from a list of paths.

        :param texpaths: a path separated (':' on Linux) list of files or
                         directories to export

        :param output: the output path name, or standard out if not given

        """
        extractor = None
        entries: Dict[str, Dict[str, str]] = {}
        self._set_log_level_info()
        for path in map(Path, texpaths.split(os.pathsep)):
            if path.exists():
                if logger.isEnabledFor(logging.INFO):
                    logger.info(f'exporting {path}')
                extractor = self.get_extractor(path)
                ex_entries: Dict[str, Dict[str, str]] = extractor.extracted_entries
                entries.update(ex_entries)
                logger.info(f'parsed {len(ex_entries)} entries from {path}')
                if logger.isEnabledFor(logging.DEBUG):
                    keys = ', '.join(ex_entries.keys())
                    logger.debug(f'keys: {keys}')
            else:
                logger.warning(f'file or directory missing: {path}--skipping')
        if logger.isEnabledFor(logging.DEBUG):
            keys = ', '.join(entries.keys())
            logger.debug(f'creating extracted file with: {keys}')
        if output is None:
            extractor.extract(extracted_entries=entries)
        else:
            with open(output, 'w') as f:
                extractor.extract(writer=f, extracted_entries=entries)
        if output is not None:
            logger.info(f'wrote {output}')
