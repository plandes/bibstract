"""This utility extracts Bib(La)Tex references (a.k.a *markers*) from a
(La)Tex.

"""
__author__ = 'Paul Landes'

from dataclasses import dataclass, field
import logging
from pathlib import Path
from zensols.config import ConfigFactory
from . import Extractor

logger = logging.getLogger(__name__)


@dataclass
class Exporter(object):
    """This utility extracts Bib(La)Tex references (a.k.a *markers*) from a
    (La)Tex.

    """
    CLI_META = {'mnemonic_excludes': {'get_extractor'},
                'mnemonic_overrides': {'print_bibtex_ids': 'showbib',
                                       'print_texfile_refs': 'showtex',
                                       'print_extracted_ids': 'showextract'},
                'option_includes': {}}

    config_factory: ConfigFactory = field()
    """The configuration factory used to create this instance."""

    master_bib: Path = field()
    """The path to the master BibTex file."""

    log_name: str = field()
    """The name of the package logger."""

    def get_extractor(self, texpath: Path = None) -> Extractor:
        return self.config_factory.new_instance(
            'extractor', self.master_bib, texpath=texpath)

    def _set_log_level_info(self):
        logging.getLogger(self.log_name).setLevel(logging.INFO)

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

    def export(self, texpath: Path):
        """Export the derived BibTex file.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        """
        self._set_log_level_info()
        extractor = self.get_extractor(texpath)
        extractor.extract()