import sys
import unittest
from zensols.cli import CliHarness
from zensols.bibstract import Exporter, ApplicationFactory


class TestBase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = sys.maxsize
        if not hasattr(self, 'CONF'):
            self.CONF = 'test-resources/default.conf'
        harn: CliHarness = ApplicationFactory.create_harness()
        self.app: Exporter = harn.get_instance(
            f'-c {self.CONF} converters --level warn')
