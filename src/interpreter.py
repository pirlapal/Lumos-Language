"""
Lumos Interpreter - Execution Engine
Author: Gunjan Shankarbhai Purohit
"""

import sys
from runtime import Environment, RuntimeError
from ast_nodes import *


class Interpreter:

    def __init__(self):

        self.global_env = Environment()
        self.current_env = self.global_env

    def interpret(self, ast):

        self.visit(ast)

    def visit(self, node):

        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):

        raise RuntimeError(f"No visit method for {type(node).__name__}")


    def visit_Program(self, node):

        for statement in node.statements:
            self.visit(statement)



    def visit_AssignmentStatement(self, node):

        value = self.visit(node.expression)

        if self.current_env.exists(node.identifier):
            self.current_env.set(node.identifier, value)
        else:
            self.current_env.define(node.identifier, value)

    def visit_PrintStatement(self, node):

        value = self.visit(node.expression)
        print(self.value_to_string(value))

    def visit_ExpressionStatement(self, node):

        self.visit(node.expression)

    def visit_IfStatement(self, node):

        condition = self.visit(node.condition)

        if self.is_truthy(condition):
            self.visit(node.then_block)
        elif node.else_block:
            self.visit(node.else_block)

    def visit_WhileStatement(self, node):

        while self.is_truthy(self.visit(node.condition)):
            self.visit(node.body)

    def visit_ForStatement(self, node):

        loop_env = Environment(self.current_env)
        previous_env = self.current_env
        self.current_env = loop_env

        try:

            self.visit(node.init)


            while self.is_truthy(self.visit(node.condition)):
                self.visit(node.body)
                self.visit(node.update)
        finally:

            self.current_env = previous_env

    def visit_Block(self, node):

        block_env = Environment(self.current_env)
        previous_env = self.current_env
        self.current_env = block_env

        try:
            for statement in node.statements:
                self.visit(statement)
        finally:

            self.current_env = previous_env



    def visit_BinaryExpression(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.operator


        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise RuntimeError("Division by zero")

            if isinstance(left, int) and isinstance(right, int):
                return left // right
            return left / right


        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right


        elif op == 'and':
            return self.is_truthy(left) and self.is_truthy(right)
        elif op == 'or':
            return self.is_truthy(left) or self.is_truthy(right)

        else:
            raise RuntimeError(f"Unknown binary operator: {op}")

    def visit_UnaryExpression(self, node):

        operand = self.visit(node.operand)
        op = node.operator

        if op == '-':
            return -operand
        elif op == 'not':
            return not self.is_truthy(operand)
        else:
            raise RuntimeError(f"Unknown unary operator: {op}")

    def visit_TernaryExpression(self, node):

        condition = self.visit(node.condition)

        if self.is_truthy(condition):
            return self.visit(node.true_expr)
        else:
            return self.visit(node.false_expr)

    def visit_Identifier(self, node):

        return self.current_env.get(node.name)

    def visit_IntegerLiteral(self, node):

        return node.value

    def visit_FloatLiteral(self, node):

        return node.value

    def visit_StringLiteral(self, node):

        return node.value

    def visit_BooleanLiteral(self, node):

        return node.value


    def is_truthy(self, value):

        if value is None or value is False:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

    def value_to_string(self, value):

        if isinstance(value, bool):
            return 'true' if value else 'false'
        elif value is None:
            return 'null'
        elif isinstance(value, str):
            return value
        else:
            return str(value)
