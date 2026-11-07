"""
Lumos Runtime Environment
Author: Sairaj Vinod Dalvi
"""


class RuntimeError(Exception):
    pass


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise RuntimeError(f"Undefined variable '{name}'")

    def set(self, name, value):
        if name in self.variables:
            self.variables[name] = value
            return

        if self.parent is not None:
            self.parent.set(name, value)
            return

        raise RuntimeError(f"Undefined variable '{name}'")

    def exists(self, name):
        if name in self.variables:
            return True

        if self.parent is not None:
            return self.parent.exists(name)

        return False
