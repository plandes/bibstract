from pathlib import Path
from zensols.pybuild import SetupUtil

su = SetupUtil(
    setup_path=Path(__file__).parent.absolute(),
    name="zensols.bibstract",
    package_names=['zensols', 'resources'],
    # package_data={'': ['*.html', '*.js', '*.css', '*.map', '*.svg']},
    package_data={'': ['*.conf', '*.json', '*.yml']},
    description='This utility extracts Bib(La)Tex references (a.k.a *markers*) from a (La)Tex.',
    user='plandes',
    project='bibstract',
    keywords=['tooling'],
    # has_entry_points=False,
).setup()
