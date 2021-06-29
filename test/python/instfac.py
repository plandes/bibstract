"""Contains a utility class to create instances.

"""
__author__ = 'Paul Landes'

import logging
from typing import Any, List
from dataclasses import dataclass, field
from pathlib import Path
from zensols.cli import Application, ApplicationFactory, ApplicationResult
from zensols.bibstract import BibstractApplicationFactory

logger = logging.getLogger(__name__)


@dataclass
class InstanceFactory(object):
    args: List[str] = field(default_factory=list)
    """The command line arguments."""

    config_file: Path = field(default=Path('test-resources/bibstract.conf'))
    """The path to the test configuration file."""

    root_dir: Path = Path('.')
    """The root directory."""

    reload_factory: bool = field(default=True)
    """Whether or not to reload classes."""

    @property
    def factory(self) -> ApplicationFactory:
        return BibstractApplicationFactory.instance(
            root_dir=self.root_dir,
            reload_factory=self.reload_factory)

    def invoke(self) -> ApplicationResult:
        factory: ApplicationFactory = self.factory
        app: Application = factory.create(self.args)
        return app.invoke()

    def instance(self) -> Any:
        args = list(self.args)
        args.extend(['-c', str(self.config_file)])
        factory: ApplicationFactory = self.factory
        try:
            app: Application = factory.create(args)
            res, invokable = app.invoke_but_second_pass()
            return invokable.instance
        except SystemExit as e:
            raise ValueError(f'commnd line error: {e}')
