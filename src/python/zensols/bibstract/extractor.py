"""Extract BibTex references from a Tex file and add them from a master BibTex file.

"""
__author__ = 'plandes'

import sys
import logging
import re
from pathlib import Path
from io import TextIOWrapper
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from zensols.actioncli import persisted

logger = logging.getLogger(__name__)


class RegexFileParser(object):
    def __init__(self, pattern: re.Pattern, collector: set):
        self.pattern = pattern
        self.collector = collector

    def find(self, fileobj: TextIOWrapper):
        for line in fileobj.readlines():
            refs = self.pattern.findall(line)
            self.collector.update(refs)


class Extractor(object):
    TEX_FILE_REGEX = re.compile(r'.+\.(?:tex|sty|cls)$')
    REF_REGEX = re.compile(r'\{([a-zA-Z0-9]+?)\}')

    def __init__(self, master_bib: Path, texpath: Path):
        self.master_bib = master_bib
        self.texpath = texpath

    @property
    @persisted('_database')
    def database(self) -> BibDatabase:
        logger.info(f'parsing master bibtex file: {self.master_bib}')
        with open(self.master_bib) as f:
            return bibtexparser.load(f)

    @property
    def bibtex_ids(self) -> iter:
        return map(lambda e: e['ID'], self.database.entries)

    def _is_tex_file(self, path: Path) -> bool:
        return path.is_file() and \
            self.TEX_FILE_REGEX.match(path.name) is not None

    @property
    def tex_refs(self) -> set:
        tex_refs = set()
        parser = RegexFileParser(self.REF_REGEX, tex_refs)
        path = self.texpath
        logger.info(f'parsing references from Tex file: {path}')
        if path.is_file():
            paths = (path,)
        elif path.is_dir():
            paths = tuple(filter(self._is_tex_file, path.rglob('*')))
        logger.debug(f'parsing references from Tex files: {paths}')
        for path in paths:
            with open(path) as f:
                parser.find(f)
        return tex_refs

    @property
    def export_ids(self) -> set:
        bib = set(self.bibtex_ids)
        trefs = self.tex_refs
        return bib & trefs

    def print_bibtex_ids(self):
        logging.getLogger('bibtexparser').setLevel(logging.ERROR)
        for id in self.bibtex_ids:
            print(id)

    def print_texfile_refs(self):
        for ref in self.tex_refs:
            print(ref)

    def print_exported_ids(self):
        for id in self.export_ids:
            print(id)

    def export(self, writer=sys.stdout):
        bwriter = BibTexWriter()
        db = self.database.get_entry_dict()
        for id in sorted(self.export_ids):
            entry = db[id]
            logger.info(f'writing entry {id}')
            writer.write(bwriter._entry_to_bibtex(entry))
            logger.debug(f'exporting: {id}: <{entry}>')
        writer.flush()
