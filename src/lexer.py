"""
Lexical Analyzer for Lumos language
Author: Sairaj Vinod Dalvi
Date: March 31, 2026
"""

import re
from tokens import Token, TokenType, is_keyword, get_keyword_type


class LexerError(Exception):

    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexical error at line {line}, column {column}: {message}")


class Lexer:

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.errors = []

    def current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def peek_char(self, offset=1):
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            self.advance()

    def read_number(self):
        start_line = self.line
        start_column = self.column
        num_str = ''

        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()

        # Check for float
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            num_str += self.current_char()
            self.advance()

            while self.current_char() and self.current_char().isdigit():
                num_str += self.current_char()
                self.advance()

            return Token(TokenType.FLOAT, float(num_str), start_line, start_column)

        return Token(TokenType.INTEGER, int(num_str), start_line, start_column)

    def read_identifier(self):
        start_line = self.line
        start_column = self.column
        id_str = ''

        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()

        if is_keyword(id_str):
            token_type = get_keyword_type(id_str)
            # For boolean keywords, convert value
            if token_type == TokenType.TRUE:
                return Token(token_type, True, start_line, start_column)
            elif token_type == TokenType.FALSE:
                return Token(token_type, False, start_line, start_column)
            return Token(token_type, id_str, start_line, start_column)

        return Token(TokenType.IDENTIFIER, id_str, start_line, start_column)

    def read_string(self):
        start_line = self.line
        start_column = self.column
        string_val = ''

        self.advance()

        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() is None:
                    raise LexerError('Unterminated string literal', start_line, start_column)
                if self.current_char() == 'n':
                    string_val += '\n'
                elif self.current_char() == 't':
                    string_val += '\t'
                elif self.current_char() == '"':
                    string_val += '"'
                elif self.current_char() == '\\':
                    string_val += '\\'
                else:
                    string_val += self.current_char()
                self.advance()
            else:
                string_val += self.current_char()
                self.advance()

        if self.current_char() != '"':
            raise LexerError("Unterminated string literal", start_line, start_column)

        self.advance()  # skip closing quote
        return Token(TokenType.STRING, string_val, start_line, start_column)

    def get_next_token(self):
        while self.current_char():
            if self.current_char() in ' \t\n\r':
                self.skip_whitespace()
                continue

            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue

            start_line = self.line
            start_column = self.column
            char = self.current_char()

            # Numbers
            if char.isdigit():
                return self.read_number()

            # Identifiers and keywords
            if char.isalpha() or char == '_':
                return self.read_identifier()

            # String literals
            if char == '"':
                return self.read_string()

            # Two-character operators
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQ, '==', start_line, start_column)

            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NE, '!=', start_line, start_column)

            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LE, '<=', start_line, start_column)

            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GE, '>=', start_line, start_column)

            # Single-character operators and separators
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '=': TokenType.ASSIGN,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '?': TokenType.QUESTION,
                ':': TokenType.COLON,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
            }

            if char in single_char_tokens:
                token_type = single_char_tokens[char]
                self.advance()
                return Token(token_type, char, start_line, start_column)

            # Invalid character
            error_msg = f"Invalid character: {char}"
            self.errors.append(LexerError(error_msg, start_line, start_column))
            self.advance()

        # End of file
        return Token(TokenType.EOF, None, self.line, self.column)

    def tokenize(self):
        self.tokens = []
        self.errors = []

        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            if token.type == TokenType.EOF:
                break

        if self.errors:
            return None, self.errors

        return self.tokens, None
