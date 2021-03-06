# BibTex Extract and Populate

[![Travis CI Build Status][travis-badge]][travis-link]
[![PyPI][pypi-badge]][pypi-link]
[![Python 3.7][python37-badge]][python37-link]

This utility extracts [BibTex] references (a.k.a *markers*) from a [(La)Tex]
file and copies entries from a source (a.k.a. *master* for this program) BibTex
file.  The use case is exporting all [BetterBibtex] entries to a file on your
file system, usually one that is updated as you add, remove and modify papers
in [Zotero].

**Note**:  While the use case was intended for use with Zoter and BetterBibtex,
it will work on any BibTex file.

The program does the following:
1. Parses some large master source BibTex file.
1. Parses a file or recursively all `.tex`, `.sty`, and `.cls` files
   recursively in a directory.
1. Copies the matching entries from the master source BibTex to standard out.

The program makes the assumption that the BibTex entry IDs are unique as the
matches are very loose when parsing the (La)Tex file.


## Obtaining

The easiest way to install the command line program is via the `pip` installer:
```bash
pip3 install zensols.bibstract
```

Binaries are also available on [pypi].


## Usage

This is a command line program written that has the following usage (also use
`--help`):

* Print IDs in a master source file BibTex file: `bibstract printbib -m <file.bib>`.
* Print cite references in a (La)Tex file: `bibstract printtex -t <file|directory>`
* Print IDs that will be exported from the BibTex file: `bibstract printexport -m <file.bib> -t <file|directory>`
* Export the matching entries to standard out: `bibstract export -m <file.bib> -t <file|directory>`

Note that `file.bib` is the BibTex file and the `-t` takes a file or directory
for where to find the file(s) that contain the citation references.


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## License

Copyright (c) 2020 Paul Landes

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
[travis-link]: https://travis-ci.org/plandes/bibstract
[travis-badge]: https://travis-ci.org/plandes/bibstract.svg?branch=master
[pypi]: https://pypi.org/project/zensols.bibstract/
[pypi-link]: https://pypi.python.org/pypi/zensols.bibstract
[pypi-badge]: https://img.shields.io/pypi/v/zensols.bibstract.svg
[python37-badge]: https://img.shields.io/badge/python-3.7-blue.svg
[python37-link]: https://www.python.org/downloads/release/python-370

[BetterBibtex]: https://github.com/retorquere/zotero-better-bibtex
[Zotero]: https://www.zotero.org
[BibTex]: http://www.bibtex.org
[(La)Tex]: http://www.bibtex.org
