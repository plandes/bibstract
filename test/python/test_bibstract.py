import sys
import logging
import json
import io
from pathlib import Path
import unittest
from zensols.bibstract import Extractor

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.bibfile = Path('test-resources/someproj/sty/someproj.bib')
        self.texpath = Path('test-resources/someproj')
        self.maxDiff = sys.maxsize

    def test_bibkeys(self):
        extractor = Extractor(self.bibfile, None)
        ids = tuple(extractor.bibtex_ids)
        should = 'deerwesterIndexingLatentSemantic1990', 'mikolovEfficientEstimationWord2013', 'biswasGraphBasedKeyword2018'
        self.assertEqual(should, ids)

    def test_texkeys(self):
        extractor = Extractor(None, self.texpath)
        with open('test-resources/texrefs.json') as f:
            should = sorted(json.load(f))
        ids = sorted(extractor.tex_refs)
        self.assertEqual(should, ids)

    def test_exported_ids(self):
        extractor = Extractor(self.bibfile, self.texpath)
        with open('test-resources/exported_id.json') as f:
            should = sorted(json.load(f))
        ids = sorted(extractor.export_ids)
        self.assertEqual(should, ids)

    def test_export(self):
        extractor = Extractor(self.bibfile, self.texpath)
        sio = io.StringIO()
        extractor.export(sio)
        with open('test-resources/export.bib') as f:
            should = f.read()
        self.assertEqual(should, sio.getvalue())
