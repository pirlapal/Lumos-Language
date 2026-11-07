# Implemented language behavior

## Pipeline

`src/lexer.py` tokenizes source with line/column locations. `src/parser.py` uses recursive descent to create the node types in `src/ast_nodes.py`. `src/interpreter.py` visits those nodes, storing values in chained `Environment` objects from `src/runtime.py`. `src/compiler.py` is the command-line driver.

- Values: integers, floats, quoted strings with escapes, and `true`/`false`.
- Statements: assignment, print, expression statements, blocks, if/else, while, and for.
- Operators: arithmetic, comparisons, equality, logical operations, unary minus/not, and ternary conditionals.
- `//` begins a line comment. Semicolons terminate simple statements.
- `for` has `initialization; condition; update` syntax, with **no semicolon after the update**.
- AST output is JSON surrounded by CLI section headings. It is an inspection view, not a JSON-only API.

## Semantics to know

- Two integer operands use floor division: `7 / 2` is `3`, `-7 / 2` is `-4`. A float operand enables floating-point division.
- Conditions and logical operators use truthiness. Both operands of `and`/`or` are evaluated; they do not short-circuit. The ternary evaluates only its selected branch.
- A new name is defined in the current scope. Assignment to an existing name updates its nearest enclosing binding; it does not shadow it. Names created inside blocks are local to that block. For-loops have a loop environment.
- Operations inherit Python value behavior (for example, string concatenation is accepted). There is no separate static type checker or exhaustive runtime type system.
- Variables must exist before they are read. Undefined names and division by zero report runtime errors.
- This version has no functions, classes, modules, collections, native code generation, or language server.
- The driver returns exit status 0 for success, 1 for file/lexical/parse/runtime errors, and 2 for invalid CLI arguments. Diagnostics go to stderr; program output goes to stdout.
- Evaluation has no instruction/resource budget. Tests impose subprocess timeouts, but arbitrary programs can loop indefinitely. This is a local educational interpreter, not a sandbox or hosted code-execution service.

The historical grammar and token specification are retained in this folder. Grammar corrections for the public edition align for-loop headers, standalone blocks, and documented semantics with the implementation. The runtime code remains the source of truth for edge cases not specified there.
