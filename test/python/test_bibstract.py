import logging
import sys
import json
from pathlib import Path
from io import StringIO
import unittest
from zensols.bibstract import Exporter, Extractor
from instfac import InstanceFactory

if 0:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)


class TestMainApplication(unittest.TestCase):
    def setUp(self):
        texpath = Path('test-resources/someproj')
        self.app: Exporter = InstanceFactory(
            ('-c test-resources/bibstract.conf --level warn ' +
             'export pacify').split(),
            reload_factory=False).instance()
        self.maxDiff = sys.maxsize
        self.extractor: Extractor = self.app.get_extractor(texpath)

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

    def test_export(self):
        sio = StringIO()
        self.extractor.extract(sio)
        with open('test-resources/export.bib') as f:
            should = f.read()
        self.assertEqual(should, sio.getvalue())
