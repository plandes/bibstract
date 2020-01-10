"""Extract BibTex references from a Tex file and add them from a master BibTex file.

"""
__author__ = 'plandes'

import logging
from zensols.actioncli import persisted
from pathlib import Path
import bibtexparser

logger = logging.getLogger(__name__)


class Extractor(object):
    def __init__(self, master_bib: Path):
        self.master_bib = master_bib

    @property
    @persisted('_database')
    def database(self):
        logger.info(f'parsing master bibtex file: {self.master_bib}')
        with open(self.master_bib) as f:
            return bibtexparser.load(f)

    @property
    def ids(self):
        return map(lambda e: e['ID'], self.database.entries)

    def print_ids(self):
        logging.getLogger('bibtexparser').setLevel(logging.ERROR)
        for id in self.ids:
            print(id)

    def tmp(self):
        self.print_ids()
