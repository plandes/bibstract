"""Find packages used in the tex path.

"""
__author__ = 'Paul Landes'

from typing import Set, Union
from dataclasses import dataclass, field
import logging
import re
from pathlib import Path
from . import TexPathIterator, RegexFileParser

logger = logging.getLogger(__name__)


@dataclass
class PackageFinder(TexPathIterator):
    """Find packages used in the tex path.

    """
    package_regex: Union[str, re.Pattern] = field(default=re.compile(r'.*'))
    """The regular expression used to filter what to return

    """
    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.package_regex, str):
            self.package_regex = re.compile(self.package_regex)

    def _get_use_packages(self) -> Set[str]:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'finding packages in {self.texpaths}')
        pattern: re.Pattern = re.compile(r'\\usepackage{([a-zA-Z0-9,-]+?)\}')
        parser = RegexFileParser(pattern=pattern)
        path: Path
        for path in self._get_tex_paths():
            with open(path) as f:
                parser.find(f)
        return parser.collector

    def __call__(self) -> Set[str]:
        pks: Set[str] = self._get_use_packages()
        pks = filter(lambda s: self.package_regex.match(s) is not None, pks)
        return set(pks)
