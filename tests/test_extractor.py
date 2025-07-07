from typing import Dict
import json
from pathlib import Path
from io import StringIO
from util import TestBase
from zensols.bibstract import Extractor


class TestExtractorBase(TestBase):
    def setUp(self):
        super().setUp()
        self.extractor: Extractor = self.app._get_extractor(
            Path('test-resources/someproj'))

    def _get_entry(self, key):
        entry = self.extractor.get_entry(key)
        self.assertEqual(dict, type(entry))
        return entry


class TestExtractor(TestExtractorBase):
    def test_bibkeys(self):
        ids = tuple(self.extractor.bibtex_ids)
        should = 'deerwesterIndexingLatentSemantic1990', \
            'mikolovEfficientEstimationWord2013', \
            'mikolovAdvancesPreTrainingDistributed2017', \
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


class TestExport(TestExtractorBase):
    def test_export(self):
        sio = StringIO()
        self.extractor.extract(sio)
        with open('test-resources/export.bib') as f:
            should = f.read()
        self.assertEqual(should, sio.getvalue())


class TestDateYearConverters(TestExtractorBase):
    def setUp(self):
        self.CONF = 'test-resources/date-year-conv.conf'
        super().setUp()

    def test_converter(self):
        with open('test-resources/date-convert.json') as f:
            should = json.load(f)
        id_to_dates = {}
        # print()
        # from pprint import pprint
        for bid, entry in self.extractor.extracted_entries.items():
            #pprint(entry)
            id_to_dates[bid] = f"{entry['date']} -> {entry['year']}"
        self.assertEqual(should, id_to_dates)


class TestConditionalConverter(TestExtractorBase):
    NON_ARXIV = 'deerwesterIndexingLatentSemantic1990'
    ARXIV = 'mikolovAdvancesPreTrainingDistributed2017'

    def _test_fallthrough(self):
        entry = self._get_entry(self.NON_ARXIV)
        self.assertEqual('article', entry['ENTRYTYPE'])
        entry = self._get_entry(self.ARXIV)
        self.assertEqual('online', entry['ENTRYTYPE'])

    def _test_update(self):
        entry = self._get_entry(self.NON_ARXIV)
        self.assertEqual('article', entry['ENTRYTYPE'])
        entry = self._get_entry(self.ARXIV)
        self.assertEqual('misc', entry['ENTRYTYPE'])


class TestConditionalFallthrough(TestConditionalConverter):
    def setUp(self):
        self.CONF = 'test-resources/cond-conv-fallthrough-1.conf'
        super().setUp()

    def test_converter(self):
        self._test_fallthrough()


class TestConditionalFallthrough2(TestConditionalConverter):
    def setUp(self):
        self.CONF = 'test-resources/cond-conv-fallthrough-2.conf'
        super().setUp()

    def test_converter(self):
        self._test_fallthrough()


class TestConditionalUpdate(TestConditionalConverter):
    def setUp(self):
        self.CONF = 'test-resources/cond-conv-update.conf'
        super().setUp()

    def test_converter(self):
        self._test_update()


class TestConditionalUpdateWithUpdate(TestConditionalConverter):
    def setUp(self):
        self.CONF = 'test-resources/cond-conv-update-with-exclude.conf'
        super().setUp()

    def test_converter(self):
        self._test_update()


class TestNoReplace(TestExtractorBase):
    def test_replace(self):
        entry: Dict[str, str] = self._get_entry('biswasGraphBasedKeyword2018')
        should = 'Centrality measure,Graph based model,Keyword extraction,Sentiment analysis,Text mining'
        self.assertEqual(should, entry['keywords'])


class TestReplace(TestExtractorBase):
    def setUp(self):
        self.CONF = 'test-resources/replace.conf'
        super().setUp()

    def test_replace(self):
        entry: Dict[str, str] = self._get_entry('biswasGraphBasedKeyword2018')
        should = 'C<tr>ality measure,Graph based model,Keyword extraction,S<ti>m<t >analysis,Text mining'
        self.assertEqual(should, entry['keywords'])
