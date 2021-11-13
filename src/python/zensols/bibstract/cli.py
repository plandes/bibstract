"""Command line entry point to the application.

"""
__author__ = 'Paul Landes'

from typing import List, Any, Dict
from dataclasses import dataclass
import sys
from zensols.cli import ApplicationFactory, ActionResult, CliHarness


@dataclass
class ApplicationFactory(ApplicationFactory):
    def __init__(self, *args, **kwargs):
        kwargs['package_resource'] = 'zensols.bibstract'
        super().__init__(*args, **kwargs)


def main(args: List[str] = sys.argv, **kwargs: Dict[str, Any]) -> ActionResult:
    cli = ApplicationFactory.instance(**kwargs)
    cli.invoke(args)
