"""Behavior checks for the public CLI and documented interpreter semantics."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / 'src' / 'compiler.py'

class PublicEditionTests(unittest.TestCase):
    def run_source(self, source, *options):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'program.lumos'
            path.write_text(source, encoding='utf-8')
            return subprocess.run([sys.executable, str(DRIVER), str(path), *options], cwd=directory, capture_output=True, text=True, timeout=5)

    def assert_output(self, source, expected):
        result = self.run_source(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, '')

    def test_precedence(self):
        self.assert_output('print(2 + 3 * 4); print((2 + 3) * 4);', '14\n20\n')

    def test_division_semantics(self):
        self.assert_output('print(7 / 2); print(-7 / 2); print(7.0 / 2);', '3\n-4\n3.5\n')

    def test_boolean_and_ternary(self):
        self.assert_output('print(true and not false); print(false or true); print(false ? missing : "ok");', 'true\ntrue\nok\n')

    def test_loops_and_parent_scope_assignment(self):
        self.assert_output('total = 0; for (i = 1; i <= 4; i = i + 1) { total = total + i; } while (total < 12) total = total + 1; print(total);', '12\n')

    def test_nested_scopes(self):
        self.assert_output('x = 1; if (true) { x = 2; local = 3; print(local); } print(x);', '3\n2\n')

    def test_block_local_does_not_escape(self):
        result = self.run_source('if (true) { local = 3; } print(local);')
        self.assertEqual(result.returncode, 1)
        self.assertIn("Undefined variable 'local'", result.stderr)

    def test_unicode_and_escaped_strings(self):
        self.assert_output('print("Lumos ☀"); print("a\\nb");', 'Lumos ☀\na\nb\n')

    def test_division_by_zero_reported_once(self):
        result = self.run_source('print(1 / 0);')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr.count('Division by zero'), 1)

    def test_missing_semicolon(self):
        result = self.run_source('x = 2')
        self.assertEqual(result.returncode, 1)
        self.assertIn('PARSE ERROR', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_invalid_character(self):
        result = self.run_source('@')
        self.assertEqual(result.returncode, 1)
        self.assertIn('LEXICAL ERRORS', result.stderr)

    def test_unterminated_string_and_trailing_escape(self):
        for source in ['print("unfinished', 'print("unfinished' + chr(92)]:
            with self.subTest(source=source):
                result = self.run_source(source)
                self.assertEqual(result.returncode, 1)
                self.assertIn('Unterminated string literal', result.stderr)
                self.assertNotIn('TypeError', result.stderr)

    def test_parse_only_does_not_execute(self):
        result = self.run_source('print(missing);', '--parse-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_ast_represents_source(self):
        result = self.run_source('x = 42;', '--parse-only', '--ast')
        self.assertEqual(result.returncode, 0, result.stderr)
        start, end = result.stdout.index('{'), result.stdout.rindex('}') + 1
        ast = json.loads(result.stdout[start:end])
        self.assertEqual(ast['type'], 'Program')
        self.assertEqual(ast['statements'][0]['identifier'], 'x')
        self.assertEqual(ast['statements'][0]['expression']['value'], 42)

    def test_verbose_includes_tokens_and_output(self):
        result = self.run_source('print(9);', '--verbose')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('TOKENS', result.stdout)
        self.assertIn('PROGRAM OUTPUT', result.stdout)
        self.assertIn('\n9\n', result.stdout)

    def test_unknown_option_is_not_silently_ignored(self):
        result = self.run_source('print(1);', '--typo')
        self.assertEqual(result.returncode, 2)
        self.assertIn('unrecognized arguments', result.stderr)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(DRIVER), str(Path(directory) / 'absent.lumos')], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 1)
        self.assertIn('not found', result.stderr)

    def test_eager_boolean_evaluation_is_documented(self):
        result = self.run_source('print(false and missing);')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Undefined variable', result.stderr)

if __name__ == '__main__':
    unittest.main()
