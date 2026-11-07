# Lumos Language

An educational programming language implemented in Python: a handwritten **lexer → recursive-descent parser → abstract syntax tree → tree-walking interpreter**.

Lumos supports variables, integers, floats, strings, booleans, expressions, conditionals, ternaries, `for`/`while` loops, and block scopes. Run a program, inspect its tokens/AST, or parse it without execution. No external packages, generated parser, or build step are required.

This public edition is derived from the **SER502 Team 6 — Lumos** course project. It preserves the team's source and attribution while improving setup, test portability, and CLI diagnostics.

## Quick start

Requires Python 3.10+ (validated locally with Python 3.14).

```sh
git clone https://github.com/pirlapal/Lumos-Language.git
cd Lumos-Language
python3 src/compiler.py examples/demo.lumos
```

No `pip install` is necessary. `requirements.txt` is intentionally comment-only.

## A small Lumos program

```lumos
total = 0;
for (i = 1; i <= 5; i = i + 1) {
    total = total + i;
}
print(total);
print(total > 10 ? "Above ten" : "Ten or less");
```

Output:

```text
15
Above ten
```

Save it to a UTF-8 `.lumos` file and pass that path to `src/compiler.py`.

## Inspect the pipeline

```sh
# Execute a sample
python3 src/compiler.py examples/test_arithmetic.lumos

# Show AST, then execute
python3 src/compiler.py examples/test_loops.lumos --ast

# Inspect tokens, parsing, and program output
python3 src/compiler.py examples/test_conditionals.lumos --verbose

# Parse and display the AST without executing
python3 src/compiler.py examples/test_variables.lumos --parse-only --ast

# List command-line options
python3 src/compiler.py --help
```

The driver is named `compiler.py` in the original project, but execution is interpreted: it does not produce native machine code or bytecode. The implementation is handwritten Python, not ANTLR-generated code.

## Tests

```sh
python3 tests/check.py
```

The runner executes 41 retained parser cases, five retained runtime checks, five sample-program smoke checks, and 17 public-edition behavior tests. Suites have timeouts. The new checks cover scope, loops, precedence, AST content, parse-only mode, Unicode input, CLI errors, and lexical/runtime diagnostics. Passing these checks is not a claim of full language conformance or coverage.

Individual commands:

```sh
python3 tests/test_parser.py
python3 tests/test_runtime.py
python3 tests/test_all.py
python3 -m unittest discover -s tests -p test_regressions.py -v
```

An optional GitHub Actions template is in [docs/ci.example.yml](docs/ci.example.yml). It is not active because the publishing token lacks workflow permission. To enable it, move it to `.github/workflows/ci.yml` with an appropriately authorized account. No hosted CI result is claimed.

## Structure

```text
src/          Lexer, parser, AST, runtime, interpreter, CLI driver
examples/     Five feature samples and the original combined demo
tests/       Parser/runtime suites, behavior tests, unified runner
docs/         Grammar, tokens, team contribution record, cleanup notes
```

See [language semantics and limitations](docs/LANGUAGE.md), [grammar](docs/grammar.txt), and [public-copy changes](docs/PUBLIC_COPY.md).

## Team and attribution

Original team: Shreyas Jagannath Revankar, Sairaj Vinod Dalvi, Gunjan Shankarbhai Purohit, and Pranav Kishor Irlapale.

The original [contribution record](docs/contribution.txt) credits Pranav with loop parsing, parser integration, runtime tests, documentation, and project coordination. It also records the other team members' contributions. These are team-documented responsibilities, not a claim that one person authored the whole system. Original source author headers are preserved.

[Original project demonstration video](https://youtu.be/rK5pm6MpsI8) — retained from the source README; the video has not been revalidated for this edition.

See [NOTICE](NOTICE) for provenance and licensing status. The upstream repository supplied no software license; no new blanket license grant is added here.
