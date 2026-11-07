"""
Lumos Compiler - Main Driver
Author: Shreyas Jagannath Revankar
"""

import argparse
import sys
import json
from lexer import Lexer, LexerError
from parser import Parser, ParserError
from interpreter import Interpreter
from runtime import RuntimeError


def print_tokens(tokens):

    print("\n" + "=" * 60)
    print("TOKENS")
    print("=" * 60)
    for token in tokens:
        if token.type.name != 'EOF':
            print(f"{token.line}:{token.column}\t{token.type.name:15}\t{repr(token.value)}")
    print("=" * 60)


def print_ast(ast, indent=0):

    ast_dict = ast.to_dict()
    print(json.dumps(ast_dict, indent=2))


def compile_file(filename, verbose=False, execute=True, show_ast=False):

    try:

        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()

        if verbose:
            print(f"\nCompiling: {filename}")
            print("=" * 60)


        lexer = Lexer(source_code)
        tokens, lex_errors = lexer.tokenize()

        if lex_errors:
            print("\nLEXICAL ERRORS:", file=sys.stderr)
            for error in lex_errors:
                print(f"  {error}", file=sys.stderr)
            return None

        if verbose:
            print_tokens(tokens)


        parser = Parser(tokens)
        try:
            ast = parser.parse()

            if verbose:
                print("\n" + "=" * 60)
                print("PARSING SUCCESSFUL")
                print("=" * 60)

            if show_ast:
                print("\n" + "=" * 60)
                print("ABSTRACT SYNTAX TREE")
                print("=" * 60)
                print_ast(ast)
                print("=" * 60)

            if execute:
                if verbose or show_ast:
                    print("\n" + "=" * 60)
                    print("PROGRAM OUTPUT")
                    print("=" * 60)

                interpreter = Interpreter()
                try:
                    interpreter.interpret(ast)
                except RuntimeError as e:
                    print(f"\nRUNTIME ERROR: {e}", file=sys.stderr)
                    return None

                if verbose or show_ast:
                    print("=" * 60)

            return ast

        except ParserError as e:
            print(f"\nPARSE ERROR: {e}", file=sys.stderr)
            return None

    except LexerError as e:
        print(f"LEXICAL ERROR: {e}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main():
    options = argparse.ArgumentParser(description='Parse and interpret a Lumos source file.')
    options.add_argument('source_file', help='UTF-8 .lumos source file')
    options.add_argument('--verbose', '-v', action='store_true', help='Show tokens and compilation details')
    options.add_argument('--ast', action='store_true', help='Display the AST as JSON')
    options.add_argument('--parse-only', action='store_true', help='Parse without executing the program')
    args = options.parse_args()
    ast = compile_file(args.source_file, verbose=args.verbose, execute=not args.parse_only, show_ast=args.ast)
    return 0 if ast is not None else 1


if __name__ == "__main__":
    sys.exit(main())
