from typing import Set
from pathlib import Path
from zensols.bibstract import PackageFinder
from util import TestBase


class TestPackage(TestBase):
    def setUp(self):
        super().setUp()
        base = Path('test-resources')
        self.pkg_finder: PackageFinder = self.app._get_package_finder(
            base, '^zen', None)
        self.dep_resolver: PackageFinder = self.app._get_package_finder(
            base, '^zen', base / 'lib')

    def test_package_find(self):
        pkgs: Set[str] = self.pkg_finder.get_packages()
        should = ['zenacademic', 'zenacro', 'zenfig', 'zenhref', 'zenlist',
                  'zenmath', 'zenreport', 'zensec']
        self.assertEqual(set(should), pkgs)

    def test_deps(self):
        pkgs: Set[str] = self.dep_resolver.get_packages()
        should = ['zenacademic', 'zenacro', 'zenfig', 'zenmath',
                  'zenreport', 'zensec']
        self.assertEqual(set(should), pkgs)

    def test_deps_inverse(self):
        self.dep_resolver.inverse = True
        pkgs: Set[str] = self.dep_resolver.get_packages()
        should = ['zenhref', 'zenletter', 'zenlist', 'zenlisting', 'zennlp',
                  'zennohref', 'zenpronoun', 'zenslides', 'zentable']
        self.assertEqual(set(should), pkgs)
