# Public edition cleanup

The original private repository is unchanged. This edition uses fresh Git history and retains all seven runtime source modules, six Lumos examples, useful text specifications, tests, and attribution.

## Organization

- `data/` → `examples/` and the combined demo moved into that folder.
- `doc/` → `docs/`, retaining grammar, tokens, and contribution notes.
- Root test scripts → `tests/`, with paths anchored to the repository and subprocesses using the active Python interpreter.
- Removed empty `.placeholder` files and duplicate course presentation/design PDFs; retained the editable text specifications and contribution evidence.
- Corrected malformed `requirements.txt`; this project needs no external dependency installation.
- Replaced milestone-heavy README sections and obsolete ANTLR claims with actual setup and implementation details.
- Removed the team email list from the contribution record; names and responsibilities remain.

## Small correctness fixes

- A trailing escape in an unterminated string now yields a lexical error rather than a Python TypeError.
- CLI diagnostics consistently use stderr. Runtime errors are reported once.
- Added argparse options/help and rejection of unknown options, preserving the existing execution modes.
- Source files are read as UTF-8.
- Removed the lexer's broken standalone demo entry point that referenced an undefined variable.
- Runtime checks now use isolated temporary files and include the previously uncalled comprehensive test.
- Removed duplicate parser-suite invocation and added behavior checks that verify real CLI output and failure paths.
- Corrected EBNF for-loop syntax and descriptions of assignment, boolean evaluation, and string operations.

## Verification and limits

Run `python3 tests/check.py`: parser cases, runtime checks, sample smoke checks, and public-edition behavior tests. Local verification used Python 3.14. No native compiler, ANTLR dependency, hosted execution UI, performance claims, or test coverage percentage is asserted.

The CI definition is a documentation template rather than an active workflow, because the publishing token lacks workflow scope. License rights remain with the original contributors; no new software license is inferred from public visibility.
