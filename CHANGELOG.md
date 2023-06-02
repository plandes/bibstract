# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased]


## [1.0.0] - 2023-02-02
### Changed
- Updated [zensols.util] to 1.12.0.


## [0.1.1] - 2022-10-07
### Changes
- Upgrade [zensols.util] and application configuration strategy.
- More robust and various date converter fixes.

### Removed
- Support for Python 3.7, 3.8.


## [0.1.0] - 2022-05-12
### Added
- Support to find packages and packages as dependencies from LaTeX `usepackage`
  commands.
- Unit tests for new functionality, and more unit tests for the existing.

### Changed
- Combine the `exportall` in to the `export` action by supporting OS path
  separated string.

### Removed
- The `exportall` action.



## [0.0.5] - 2022-02-03
### Changed
- Upgrade the `zensols.util` CLI harness and import INI syntax.

### Added
- A converter that conditionally invokes other converters.
- A converter to use regular expressions to replace text in entry values.
- A converter to remove entry keys based on regular expressions.


## [0.0.4] - 2021-06-29
### Changed
- Upgraded to application based CLI.
- Changed name of `print`* action mnemonics to `show`*.

### Removed
- Master BibTex file is no longer available on the command line.  It must be
  given in the configuration file

### Added
- BibTex entry conversion: date to year, and field copy/moving.


## [0.0.3] - 2021-06-29
### Changed
- Upgrade to `zensols.util`.


## [0.0.2] - 2020-01-20
### Changed
- Add config resource file support.


## [0.0.1] - 2021-06-28
### Added
- Initial version.


<!-- links -->
[Unreleased]: https://github.com/plandes/bibstract/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/plandes/bibstract/compare/v0.1.1...v1.0.0
[0.1.1]: https://github.com/plandes/bibstract/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/plandes/bibstract/compare/v0.0.5...v0.1.0
[0.0.5]: https://github.com/plandes/bibstract/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/plandes/bibstract/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/plandes/bibstract/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/plandes/bibstract/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/plandes/bibstract/compare/v0.0.0...v0.0.1

[zensols.util]: https://github.com/plandes/util
