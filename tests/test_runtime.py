"""
Lumos Runtime Test Suite
Tests the execution of Lumos programs
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def run_program(filename, timeout=10):

    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / 'src' / 'compiler.py'), str(filename)],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Program timed out (possible infinite loop)"
    except Exception as e:
        return -1, "", str(e)


def test_arithmetic():
    print("Testing arithmetic operations...")
    returncode, stdout, stderr = run_program(str(ROOT / 'examples' / 'test_arithmetic.lumos'))

    if returncode != 0:
        print(f"  FAILED: {stderr}")
        return False

    expected_values = ['15', '5', '50', '2', '25', '45']
    lines = stdout.strip().split('\n')

    for expected in expected_values:
        if expected not in lines:
            print(f"  FAILED: Expected {expected} in output")
            return False

    print("  PASSED")
    return True


def test_variables():
    print("Testing variable assignments...")
    returncode, stdout, stderr = run_program(str(ROOT / 'examples' / 'test_variables.lumos'))

    if returncode != 0:
        print(f"  FAILED: {stderr}")
        return False


    if 'true' in stdout and 'false' in stdout:
        print("  PASSED")
        return True

    print("  FAILED: Expected boolean outputs")
    return False


def test_conditionals():

    print("Testing conditional statements...")
    returncode, stdout, stderr = run_program(str(ROOT / 'examples' / 'test_conditionals.lumos'))

    if returncode != 0:
        print(f"  FAILED: {stderr}")
        return False


    expected = ['Adult', 'Hot day']
    for exp in expected:
        if exp not in stdout:
            print(f"  FAILED: Expected '{exp}' in output")
            return False

    print("  PASSED")
    return True


def test_comprehensive():

    print("Testing comprehensive program...")

    returncode, stdout, stderr = run_program(str(ROOT / 'examples' / 'test_comprehensive.lumos'), timeout=20)

    if returncode != 0:
        print(f"  FAILED: {stderr}")
        return False


    if len(stdout) > 0:
        print("  PASSED")
        return True

    print("  FAILED: No output generated")
    return False


def test_error_handling():

    print("Testing error handling...")

    with tempfile.TemporaryDirectory() as directory:
        test_file = Path(directory) / 'undefined.lumos'
        test_file.write_text('print(undefined_var);', encoding='utf-8')
        returncode, stdout, stderr = run_program(test_file)

    if returncode != 0 and 'Undefined variable' in stderr:
        print("  PASSED")
        return True

    print("  FAILED: Expected runtime error for undefined variable")
    return False


def main():
    print("=" * 60)
    print("LUMOS RUNTIME TEST SUITE")
    print("=" * 60)
    print()

    tests = [
        test_arithmetic,
        test_variables,
        test_conditionals,
        test_comprehensive,
        test_error_handling
    ]

    passed = 0
    failed = 0

    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
        print()

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
