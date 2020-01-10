import logging
from pathlib import Path
import unittest
from zensols.bibstract import Extractor

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestExtractor(unittest.TestCase):
    def setUp(self):
        bibfile = Path('resources/test.bib')
        self.extractor = Extractor(bibfile)

    def test_somedata(self):
        ids = tuple(self.extractor.ids)
        should = 'mikolovEfficientEstimationWord2013', 'biswasGraphBasedKeyword2018'
        self.assertEqual(should, ids)
