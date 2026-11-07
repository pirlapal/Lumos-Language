"""
Abstract Syntax Tree Node Definitions for Lumos language
Author: Pranav Kishor Irlapale
Date: March 31, 2026
"""

class ASTNode:

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict()")


class Program(ASTNode):

    def __init__(self, statements):
        self.statements = statements

    def to_dict(self):
        return {
            "type": "Program",
            "statements": [stmt.to_dict() for stmt in self.statements]
        }


class AssignmentStatement(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def to_dict(self):
        return {
            "type": "AssignmentStatement",
            "identifier": self.identifier,
            "expression": self.expression.to_dict()
        }


class PrintStatement(ASTNode):

    def __init__(self, expression):
        self.expression = expression

    def to_dict(self):
        return {
            "type": "PrintStatement",
            "expression": self.expression.to_dict()
        }


class ExpressionStatement(ASTNode):

    def __init__(self, expression):
        self.expression = expression

    def to_dict(self):
        return {
            "type": "ExpressionStatement",
            "expression": self.expression.to_dict()
        }


class IfStatement(ASTNode):

    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def to_dict(self):
        result = {
            "type": "IfStatement",
            "condition": self.condition.to_dict(),
            "then_block": self.then_block.to_dict()
        }
        if self.else_block:
            result["else_block"] = self.else_block.to_dict()
        return result


class WhileStatement(ASTNode):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "type": "WhileStatement",
            "condition": self.condition.to_dict(),
            "body": self.body.to_dict()
        }


class ForStatement(ASTNode):

    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def to_dict(self):
        return {
            "type": "ForStatement",
            "init": self.init.to_dict(),
            "condition": self.condition.to_dict(),
            "update": self.update.to_dict(),
            "body": self.body.to_dict()
        }


class Block(ASTNode):

    def __init__(self, statements):
        self.statements = statements

    def to_dict(self):
        return {
            "type": "Block",
            "statements": [stmt.to_dict() for stmt in self.statements]
        }


class BinaryExpression(ASTNode):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def to_dict(self):
        return {
            "type": "BinaryExpression",
            "operator": self.operator,
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }


class UnaryExpression(ASTNode):

    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def to_dict(self):
        return {
            "type": "UnaryExpression",
            "operator": self.operator,
            "operand": self.operand.to_dict()
        }


class TernaryExpression(ASTNode):

    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def to_dict(self):
        return {
            "type": "TernaryExpression",
            "condition": self.condition.to_dict(),
            "true_expr": self.true_expr.to_dict(),
            "false_expr": self.false_expr.to_dict()
        }


class Identifier(ASTNode):

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "type": "Identifier",
            "name": self.name
        }


class IntegerLiteral(ASTNode):

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "type": "IntegerLiteral",
            "value": self.value
        }


class FloatLiteral(ASTNode):

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "type": "FloatLiteral",
            "value": self.value
        }


class StringLiteral(ASTNode):

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "type": "StringLiteral",
            "value": self.value
        }


class BooleanLiteral(ASTNode):

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "type": "BooleanLiteral",
            "value": self.value
        }
