"""Command line entry point to the application.

"""
__author__ = 'Paul Landes'

from typing import List, Any, Dict
import sys
from zensols.cli import ApplicationFactory, ActionResult, CliHarness


class ApplicationFactory(ApplicationFactory):
    def __init__(self, *args, **kwargs):
        kwargs['package_resource'] = 'zensols.bibstract'
        super().__init__(*args, **kwargs)


def main(args: List[str] = sys.argv, **kwargs: Dict[str, Any]) -> ActionResult:
    harness: CliHarness = ApplicationFactory.create_harness(relocate=False)
    harness.invoke(args, **kwargs)
