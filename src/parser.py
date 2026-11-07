"""
Recursive Descent Parser for Lumos language
Authors: Pranav Kishor Irlapale, Shreyas Jagannath Revankar, Sairaj Dalvi
Date: March 31, 2026
"""

from tokens import TokenType
from ast_nodes import *


class ParserError(Exception):

    def __init__(self, message, token):
        self.message = message
        self.token = token
        super().__init__(
            f"Parse error at line {token.line}, column {token.column}: {message}"
        )


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None

    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]

    def peek(self, offset=1):
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def expect(self, token_type):
        if self.current_token.type != token_type:
            raise ParserError(
                f"Expected {token_type.name}, got {self.current_token.type.name}",
                self.current_token
            )
        token = self.current_token
        self.advance()
        return token

    def match(self, *token_types):
        return self.current_token.type in token_types


    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)


    def parse_statement(self):
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.PRINT):
            return self.parse_print_statement()
        elif self.match(TokenType.LBRACE):
            return self.parse_block()
        elif self.match(TokenType.IDENTIFIER):
            if self.peek() and self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()
            else:
                return self.parse_expression_statement()
        else:
            return self.parse_expression_statement()

    def parse_assignment(self):
        identifier = self.current_token.value
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        expression = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return AssignmentStatement(identifier, expression)

    def parse_print_statement(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expression = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(expression)

    def parse_expression_statement(self):
        expression = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ExpressionStatement(expression)

    def parse_if_statement(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)

        if self.match(TokenType.LBRACE):
            then_block = self.parse_block()
        else:
            stmt = self.parse_statement()
            then_block = Block([stmt])

        else_block = None
        if self.match(TokenType.ELSE):
            self.advance()
            if self.match(TokenType.LBRACE):
                else_block = self.parse_block()
            else:
                stmt = self.parse_statement()
                else_block = Block([stmt])

        return IfStatement(condition, then_block, else_block)

    def parse_while_statement(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)

        if self.match(TokenType.LBRACE):
            body = self.parse_block()
        else:
            stmt = self.parse_statement()
            body = Block([stmt])

        return WhileStatement(condition, body)

    def parse_for_statement(self):
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)

        init_id = self.current_token.value
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        init_expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        init = AssignmentStatement(init_id, init_expr)

        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        update_id = self.current_token.value
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        update_expr = self.parse_expression()
        update = AssignmentStatement(update_id, update_expr)

        self.expect(TokenType.RPAREN)

        if self.match(TokenType.LBRACE):
            body = self.parse_block()
        else:
            stmt = self.parse_statement()
            body = Block([stmt])

        return ForStatement(init, condition, update, body)

    def parse_block(self):
        self.expect(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return Block(statements)


    def parse_expression(self):
        return self.parse_ternary_expression()

    def parse_ternary_expression(self):
        expr = self.parse_logical_or_expression()

        if self.match(TokenType.QUESTION):
            self.advance()
            true_expr = self.parse_expression()
            self.expect(TokenType.COLON)
            false_expr = self.parse_expression()
            return TernaryExpression(expr, true_expr, false_expr)

        return expr

    def parse_logical_or_expression(self):
        left = self.parse_logical_and_expression()

        while self.match(TokenType.OR):
            operator = self.current_token.value
            self.advance()
            right = self.parse_logical_and_expression()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_logical_and_expression(self):
        left = self.parse_equality_expression()

        while self.match(TokenType.AND):
            operator = self.current_token.value
            self.advance()
            right = self.parse_equality_expression()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_equality_expression(self):
        left = self.parse_relational_expression()

        while self.match(TokenType.EQ, TokenType.NE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_relational_expression()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_relational_expression(self):
        left = self.parse_additive_expression()

        while self.match(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_additive_expression()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_multiplicative_expression()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_multiplicative_expression(self):
        left = self.parse_unary_expression()

        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_unary_expression()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_unary_expression(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryExpression(operator, operand)

        return self.parse_primary_expression()

    def parse_primary_expression(self):

        if self.match(TokenType.INTEGER):
            value = self.current_token.value
            self.advance()
            return IntegerLiteral(value)

        if self.match(TokenType.FLOAT):
            value = self.current_token.value
            self.advance()
            return FloatLiteral(value)

        if self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)

        if self.match(TokenType.TRUE, TokenType.FALSE):
            value = self.current_token.value
            self.advance()
            return BooleanLiteral(value)

        if self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return Identifier(name)

        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        raise ParserError(
            f"Unexpected token: {self.current_token.type.name}",
            self.current_token
        )


def main():
    from lexer import Lexer

    test_code = """
    x = 10;
    y = 20;
    if (x < y) {
        print(x);
    } else {
        print(y);
    }
    """

    lexer = Lexer(test_code)
    tokens, errors = lexer.tokenize()

    if errors:
        print("Lexical errors found:")
        for error in errors:
            print(f"  {error}")
        return

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("Parse successful!")
        print("AST:", ast.to_dict())
    except ParserError as e:
        print(f"Parser error: {e}")


if __name__ == "__main__":
    main()
