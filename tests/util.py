import sys
import unittest
from zensols.util import Failure
from zensols.cli import CliHarness
from zensols.bibstract import Application, ApplicationFactory


class TestBase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = sys.maxsize
        if not hasattr(self, 'CONF'):
            self.CONF = 'test-resources/default.conf'
        harn: CliHarness = ApplicationFactory.create_harness()
        self.app: Application = harn.get_instance(
            f'-c {self.CONF} converters --level warn')
        if isinstance(self.app, Failure):
            self.app.raise_exception()
