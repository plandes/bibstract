import sys
import json
from pathlib import Path
from io import StringIO
import unittest
from zensols.bibstract import Exporter, Extractor
from instfac import InstanceFactory


class TestBase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = sys.maxsize
        if not hasattr(self, 'CONF'):
            self.CONF = 'test-resources/bibstract.conf'
        self.app: Exporter = InstanceFactory(
            config_file=self.CONF,
            args='export _'.split(),
            reload_factory=False).instance()
        self.extractor: Extractor = self.app.get_extractor(
            Path('test-resources/someproj'))


class TestExtractor(TestBase):
    def test_bibkeys(self):
        ids = tuple(self.extractor.bibtex_ids)
        should = 'deerwesterIndexingLatentSemantic1990', \
            'mikolovEfficientEstimationWord2013', \
            'biswasGraphBasedKeyword2018', \
            'charikarClusteringMinimizeSum2004'
        self.assertEqual(should, ids)

    def test_texkeys(self):
        with open('test-resources/texrefs.json') as f:
            should = sorted(json.load(f))
        ids = sorted(self.extractor.tex_refs)
        self.assertEqual(should, ids)

    def test_extracted_ids(self):
        with open('test-resources/exported_id.json') as f:
            should = sorted(json.load(f))
        ids = sorted(self.extractor.extract_ids)
        self.assertEqual(should, ids)


class TestExport(TestBase):
    def test_export(self):
        sio = StringIO()
        self.extractor.extract(sio)
        with open('test-resources/export.bib') as f:
            should = f.read()
        self.assertEqual(should, sio.getvalue())


class TestConverters(TestBase):
    def setUp(self):
        self.CONF = 'test-resources/bibstract-bibtex.conf'
        super().setUp()

    def test_bibtex(self):
        with open('test-resources/date-convert.json') as f:
            should = json.load(f)
        id_to_dates = {}
        for bid, entry in self.extractor.entries.items():
            id_to_dates[bid] = f"{entry['date']} -> {entry['year']}"
        self.assertEqual(should, id_to_dates)
