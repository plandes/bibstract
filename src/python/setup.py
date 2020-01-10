from pathlib import Path
from zensols.pybuild import SetupUtil

SetupUtil(
    setup_path=Path(__file__).parent.absolute(),
    name="zensols.bibstract",
    package_names=['zensols', 'resources'],
    # package_data={'': ['*.html', '*.js', '*.css', '*.map', '*.svg']},
    description='Extract BibTex references from a Tex file and add them from a master BibTex file.',
    user='plandes',
    project='bibstract',
    keywords=['tooling'],
    # has_entry_points=False,
).setup()
