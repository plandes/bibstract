# BibTeX Extract and Populate

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.11][python311-badge]][python311-link]
[![Build Status][build-badge]][build-link]

This utility extracts [BibTeX] references (a.k.a *markers*) from a [(La)TeX]
file and copies entries from a source, which the *master BibTeX file*.  It also
provides easy customization to massage the entries of the BibTeX files (see
[features](#features)).  The use case is exporting all [BetterBibtex] entries
to a file on your file system, usually one that is updated as you add, remove
and modify papers in [Zotero].  While the use case was intended for use with
Zoter and BetterBibtex, it will work on any BibTeX system.

The program does the following:
1. Parses some large master source BibTeX file.
1. Parses a file or recursively all `.tex`, `.sty`, and `.cls` files
   recursively in a directory.
1. Copies the matching entries from the master source BibTeX to standard out.

The program makes the assumption that the BibTeX entry IDs are unique as the
matches are very loose when parsing the (La)TeX file.


## Features

Many features relate to modifying older entries to accommodate newer systems
(i.e. [BibLATEX]) or modifying newer entries to accommodate older systems
(i.e. [BibTex]).

Features:
* Replace or edit Unicode characters, which is useful when
  `\usepackage[utf8]{inputenc}` has no effect.
* Massage date strings.
* Remove certain entries that cause bibliography systems issues (useful for
  [BibLATEX]).
* Modify entries to normalize [arXiv] entries.



## Obtaining

The easiest way to install the command line program is via the `pip` installer:
```bash
pip3 install zensols.bibstract
```

Binaries are also available on [pypi].


## Usage

This is a command line program written that has the following usage (also use
`--help`):

* Print IDs in a master source file BibTeX file: `bibstract showbib`.
* Print cite references in a (La)TeX file: `bibstract showtex <file|directory>`
* Print IDs that will be exported from the BibTeX file: `bibstract showexport <file|directory>`
* Export the matching entries to standard out: `bibstract export <file|directory>`


## Converters

A set of *converters* can be specified in the [configuration file], which
modify each parsed BibTeX entry in succession.  Currently there the following:
* **date_year**: Converts the year part of a date field to a year.  This is
  useful when using Zotero's Better Biblatex extension that produces BibLatex
  formats, but you need BibTeX entries.
* **copy**: Copy or move one or more fields in the entry.  This is useful when
  your bibliography style expects one key, but the output (i.e.BibLatex)
  outputs a different named field). When `destructive` is set to ``True``, this
  copy operation becomes a move.

Converters can be set be set and configured in the [configuration file].  See
the [test cases](test/python) for more examples.


## Configuration

A [configuration file] must be given, whose location is either given with a
`-c` command line argument, or set in the environment variable `BIBSTRACTRC`.

An example [configuration file] is available, which has only one INI section
`default` with option `master_bib` with the master BibTeX file.


### Example Configuration File

The following example configuration file points to the a home directory file
where you tell where [BetterBibtex] to export.  It then specifies to convert
dates with years (deleting the `date` field after)when creating the output.

In addition, it copies the `journaltitle` (exported by [BetterBibtex]) to
`journal`, which is used by BibTeX.  This converter, called *replace* is
configured the `replace_converter` entry.

```ini
[default]
master_bib = ${env:home}/.zotero-betterbib.bib
converters = date_year_destructive, replace

[replace_converter]
class_name = zensols.bibstract.CopyOrMoveConverter
fields = dict: {'journaltitle': 'journal'}
destructive = False
```


## Documentation

See the [full documentation](https://plandes.github.io/bibstract/index.html).
The [API reference](https://plandes.github.io/bibstract/api.html) is also
available.


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## Community

Please star this repository and let me know how and where you use this API.
Contributions as pull requests, feedback and any input is welcome.


## License

Copyright (c) 2020 - 2025 Paul Landes

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


<!-- links -->
[pypi]: https://pypi.org/project/zensols.bibstract/
[pypi-link]: https://pypi.python.org/pypi/zensols.bibstract
[pypi-badge]: https://img.shields.io/pypi/v/zensols.bibstract.svg
[python311-badge]: https://img.shields.io/badge/python-3.11-blue.svg
[python311-link]: https://www.python.org/downloads/release/python-3110
[build-badge]: https://github.com/plandes/bibstract/workflows/CI/badge.svg
[build-link]: https://github.com/plandes/bibstract/actions

[configuration file]: #example-configuration-file
[BetterBibtex]: https://github.com/retorquere/zotero-better-bibtex
[Zotero]: https://www.zotero.org
[BibTeX]: http://www.bibtex.org
[BibLATEX]: https://ctan.org/pkg/biblatex?lang=en
[(La)TeX]: http://www.bibtex.org
[arXiv]: https://arxiv.org
