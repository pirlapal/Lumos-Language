"""
Test Runner for Lumos Compiler
Author: Pranav Kishor Irlapale
Date: April 2, 2026
"""

import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import sys


sys.path.insert(0, str(ROOT / 'src'))

from compiler import compile_file


def test_all_programs():

    test_files = [
        str(ROOT / 'examples' / 'test_arithmetic.lumos'),
        str(ROOT / 'examples' / 'test_variables.lumos'),
        str(ROOT / 'examples' / 'test_conditionals.lumos'),
        str(ROOT / 'examples' / 'test_loops.lumos'),
        str(ROOT / 'examples' / 'test_comprehensive.lumos'),
    ]

    print("=" * 80)
    print("LUMOS COMPILER TEST SUITE")
    print("=" * 80)

    passed = 0
    failed = 0
    errors = []

    for test_file in test_files:
        print(f"\nTesting: {test_file}")
        print("-" * 80)

        if not os.path.exists(test_file):
            print(f"SKIP: File not found")
            failed += 1
            errors.append(f"{test_file}: File not found")
            continue

        try:
            ast = compile_file(test_file, verbose=False)
            if ast:
                print("PASS: Compiled successfully")
                passed += 1
            else:
                print("FAIL: Compilation failed")
                failed += 1
                errors.append(f"{test_file}: Compilation failed")
        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1
            errors.append(f"{test_file}: {e}")

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total tests: {len(test_files)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")

    print("=" * 80)

    return failed == 0


def main():
    """Main entry point"""
    success = test_all_programs()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
