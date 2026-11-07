"""
Parser Test Cases for Lumos Language
Author: Shreyas Jagannath Revankar
"""

import sys
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


sys.path.insert(0, str(ROOT / 'src'))

from lexer import Lexer
from parser import Parser, ParserError
from ast_nodes import *


class TestResult:

    def __init__(self, name, passed, error=None):
        self.name = name
        self.passed = passed
        self.error = error


def run_parser_test(test_name, source_code, should_pass=True):

    try:

        lexer = Lexer(source_code)
        tokens, lex_errors = lexer.tokenize()

        if lex_errors:
            return TestResult(test_name, False, f"Lexical errors: {lex_errors}")


        parser = Parser(tokens)
        ast = parser.parse()

        if should_pass:
            return TestResult(test_name, True)
        else:
            return TestResult(test_name, False, "Expected parse error but succeeded")

    except ParserError as e:
        if should_pass:
            return TestResult(test_name, False, f"Parse error: {e}")
        else:
            return TestResult(test_name, True)
    except Exception as e:
        return TestResult(test_name, False, f"Unexpected error: {e}")


def test_literals():

    tests = []


    tests.append(run_parser_test(
        "Integer Literal",
        "x = 42;",
        True
    ))


    tests.append(run_parser_test(
        "Float Literal",
        "pi = 3.14;",
        True
    ))


    tests.append(run_parser_test(
        "String Literal",
        'message = "Hello, World!";',
        True
    ))


    tests.append(run_parser_test(
        "Boolean True",
        "flag = true;",
        True
    ))

    tests.append(run_parser_test(
        "Boolean False",
        "flag = false;",
        True
    ))

    return tests


def test_arithmetic_expressions():

    tests = []


    tests.append(run_parser_test(
        "Addition",
        "result = a + b;",
        True
    ))


    tests.append(run_parser_test(
        "Subtraction",
        "result = a - b;",
        True
    ))


    tests.append(run_parser_test(
        "Multiplication",
        "result = a * b;",
        True
    ))


    tests.append(run_parser_test(
        "Division",
        "result = a / b;",
        True
    ))


    tests.append(run_parser_test(
        "Expression Precedence",
        "result = a + b * c - d / e;",
        True
    ))


    tests.append(run_parser_test(
        "Parenthesized Expression",
        "result = (a + b) * (c - d);",
        True
    ))


    tests.append(run_parser_test(
        "Unary Minus",
        "result = -x;",
        True
    ))

    return tests


def test_relational_expressions():

    tests = []

    tests.append(run_parser_test("Less Than", "result = a < b;", True))
    tests.append(run_parser_test("Greater Than", "result = a > b;", True))
    tests.append(run_parser_test("Less or Equal", "result = a <= b;", True))
    tests.append(run_parser_test("Greater or Equal", "result = a >= b;", True))
    tests.append(run_parser_test("Equal", "result = a == b;", True))
    tests.append(run_parser_test("Not Equal", "result = a != b;", True))

    return tests


def test_logical_expressions():

    tests = []

    tests.append(run_parser_test("Logical AND", "result = a and b;", True))
    tests.append(run_parser_test("Logical OR", "result = a or b;", True))
    tests.append(run_parser_test("Logical NOT", "result = not a;", True))
    tests.append(run_parser_test(
        "Complex Logical",
        "result = (a and b) or (c and not d);",
        True
    ))

    return tests


def test_ternary_operator():

    tests = []

    tests.append(run_parser_test(
        "Simple Ternary",
        "result = x > 0 ? a : b;",
        True
    ))

    tests.append(run_parser_test(
        "Nested Ternary",
        "result = x > 10 ? a : (x > 5 ? b : c);",
        True
    ))

    return tests


def test_print_statement():

    tests = []

    tests.append(run_parser_test(
        "Print Variable",
        "print(x);",
        True
    ))

    tests.append(run_parser_test(
        "Print Expression",
        "print(x + y);",
        True
    ))

    tests.append(run_parser_test(
        "Print String",
        'print("Hello");',
        True
    ))

    return tests


def test_if_statement():

    tests = []


    tests.append(run_parser_test(
        "Simple If",
        """
        if (x > 0) {
            print(x);
        }
        """,
        True
    ))


    tests.append(run_parser_test(
        "If-Else",
        """
        if (x > 0) {
            print("positive");
        } else {
            print("negative");
        }
        """,
        True
    ))


    tests.append(run_parser_test(
        "Nested If",
        """
        if (x > 0) {
            if (x > 10) {
                print("large");
            } else {
                print("small");
            }
        }
        """,
        True
    ))


    tests.append(run_parser_test(
        "If Single Statement",
        "if (x > 0) print(x);",
        True
    ))

    return tests


def test_while_loop():

    tests = []

    tests.append(run_parser_test(
        "Simple While",
        """
        while (i < 10) {
            print(i);
            i = i + 1;
        }
        """,
        True
    ))

    tests.append(run_parser_test(
        "While Single Statement",
        "while (i < 10) i = i + 1;",
        True
    ))

    tests.append(run_parser_test(
        "Nested While",
        """
        while (i < 10) {
            while (j < 5) {
                print(j);
                j = j + 1;
            }
            i = i + 1;
        }
        """,
        True
    ))

    return tests


def test_for_loop():

    tests = []

    tests.append(run_parser_test(
        "Simple For",
        """
        for (i = 0; i < 10; i = i + 1) {
            print(i);
        }
        """,
        True
    ))

    tests.append(run_parser_test(
        "For Single Statement",
        "for (i = 0; i < 10; i = i + 1) print(i);",
        True
    ))

    tests.append(run_parser_test(
        "Nested For",
        """
        for (i = 0; i < 3; i = i + 1) {
            for (j = 0; j < 3; j = j + 1) {
                print(i * j);
            }
        }
        """,
        True
    ))

    return tests


def test_error_cases():

    tests = []


    tests.append(run_parser_test(
        "Missing Semicolon",
        "x = 10",
        False
    ))


    tests.append(run_parser_test(
        "Invalid Expression",
        "x = + ;",
        False
    ))


    tests.append(run_parser_test(
        "Unmatched Parenthesis",
        "x = (a + b;",
        False
    ))


    tests.append(run_parser_test(
        "Missing If Condition",
        "if { print(x); }",
        False
    ))

    return tests


def print_test_results(category, results):

    print(f"\n{category}")
    print("-" * 60)

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"  [{status}] {result.name}")
        if not result.passed and result.error:
            print(f"        Error: {result.error}")

    print(f"  Subtotal: {passed}/{len(results)} passed")

    return passed, failed


def main():

    print("=" * 60)
    print("LUMOS PARSER TEST SUITE")
    print("=" * 60)

    total_passed = 0
    total_failed = 0

    categories = [
        ("Literal Tests", test_literals()),
        ("Arithmetic Expression Tests", test_arithmetic_expressions()),
        ("Relational Expression Tests", test_relational_expressions()),
        ("Logical Expression Tests", test_logical_expressions()),
        ("Ternary Operator Tests", test_ternary_operator()),
        ("Print Statement Tests", test_print_statement()),
        ("If Statement Tests", test_if_statement()),
        ("While Loop Tests", test_while_loop()),
        ("For Loop Tests", test_for_loop()),
        ("Error Detection Tests", test_error_cases()),
    ]

    for category_name, category_results in categories:
        passed, failed = print_test_results(category_name, category_results)
        total_passed += passed
        total_failed += failed


    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_passed + total_failed}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {100 * total_passed / (total_passed + total_failed):.1f}%")
    print("=" * 60)

    return total_failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
