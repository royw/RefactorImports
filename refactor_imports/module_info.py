# coding=utf-8

"""
Encapsulate the information about a module.  Given the module_spec and file_spec the module
is parsed for information about it's imports and exportable symbols, and call references.
"""

import ast
import os
import re
import imp
from pprint import pformat

from refactor_imports.astpp import dump

from refactor_imports.exportable import Exportable

__author__ = 'roy'


# noinspection PyPep8Naming
class ModuleInfo(object):
    """
    Usage::

        module_info = ModuleInfo("refactor_imports.module_info", "module_info.py")
        pprint(module_info.class_names)

    """
    TEST_NUMBER = 1

    def __init__(self, module_spec, file_spec):
        """
        :param module_spec: the module_spec which is the concatenation of the package and module name.
        :type module_spec: str
        :param file_spec: the path to the module file
        :type file_spec: str
        """
        self.module_spec = module_spec
        self.file_spec = file_spec
        self.tree = ast.parse(open(file_spec).read())
        self.calls = []
        self.variable_names = []
        self.class_names = []
        self.function_names = []
        self.import_modules = {}
        self.calls_parser = ModuleInfo.CallsParser(self)
        self.calls_parser.visit(self.tree)
        self.exportable_parser = ModuleInfo.ExportableParser(self)
        self.exportable_parser.visit(self.tree)
        self.import_parser = ModuleInfo.ImportParser(self)
        self.import_parser.visit(self.tree)

    def __str__(self):
        return "module: {m} file: {f}\n{classes}".format(m=self.module_spec, f=self.file_spec,
                                                         classes=pformat(self.class_names))

    def dump_tree(self):
        """
        :return:
        :rtype:
        """
        return dump(self.tree)

    @property
    def exportables(self):
        """
        :return: list of exportable symbols
        :rtype: list(Exportable)
        """
        return [Exportable(module_spec=self.module_spec,
                           file_spec=self.file_spec,
                           name=qualified_name.split('.')[-1]) for qualified_name in self.exportable_names]

    @property
    def public_names(self):
        """
        :return: list of public class, function, and variable names
        :rtype: list(str)
        """
        return [name for name in self.defined_names if not name.startswith('_')]

    @property
    def protect_names(self):
        """
        :return: list of protected class, function, and variable names
        :rtype: list(str)
        """
        return [name for name in self.defined_names if re.match(r'^_[^_]', name)]

    @property
    def private_names(self):
        """
        :return: list of private class, function, and variable names
        :rtype: list(str)
        """
        return [name for name in self.defined_names if re.match(r'^__[^_]', name)]

    @property
    def defined_names(self):
        """
        :return: list of class, function, and variable names
        :rtype: list(str)
        """
        return list(self.class_names) + list(self.function_names) + list(self.variable_names)

    @property
    def exportable_names(self):
        """
        :return: list of public and protected class, function, and variable names
        :rtype: list(str)
        """
        return list(self.public_names) + list(self.protect_names)

    @property
    def full_names(self):
        """
        :return: list containing fully qualified exportable names
        :rtype: list(str)
        """
        return ["{module}.{name}".format(module=self.module_spec, name=name) for name in self.exportable_names]

    # noinspection PyPep8Naming,PyMethodMayBeStatic,PyDocstring
    class ImportParser(ast.NodeVisitor):
        """sets parent.symbol_hash"""

        def __init__(self, parent):
            self.parent = parent

        def continue_parsing(self, stmt):
            """
            Helper: parse a node's children

            :param stmt: AST statement
            """
            super(ModuleInfo.ImportParser, self).generic_visit(stmt)

        def visit_Import(self, stmt):
            """
            retrieve the name from the returned object
            normally, there is just a single alias

            :param stmt: AST statement
            """
            for alias in stmt.names:
                if alias.name not in self.parent.import_modules:
                    file_spec = imp.find_module(stmt.module)[1]
                    print(file_spec)
                    if os.path.isfile(file_spec):
                        info = ModuleInfo(module_spec=alias.name, file_spec=file_spec)
                        self.parent.import_modules[alias.name] = info
            self.continue_parsing(stmt)

        def visit_ImportFrom(self, stmt):
            if stmt.module not in self.parent.import_modules:
                file_spec = imp.find_module(stmt.module)[1]
                print(file_spec)
                if os.path.isfile(file_spec):
                    info = ModuleInfo(module_spec=stmt.module, file_spec=file_spec)
                    self.parent.import_modules[stmt.module] = info
            self.continue_parsing(stmt)

    # noinspection PyPep8Naming,PyDocstring
    class CallsParser(ast.NodeVisitor):
        """sets parent.calls"""

        def __init__(self, parent):
            self.parent = parent

        def continue_parsing(self, stmt):
            """
            Helper: parse a node's children

            :param stmt: AST statement
            """
            super(ModuleInfo.CallsParser, self).generic_visit(stmt)

        def attr_to_name(self, node, suffix=''):
            if isinstance(node, ast.Name):
                if suffix:
                    return node.id + '.' + suffix
                return node.id
            if isinstance(node, ast.Attribute):
                new_suffix = node.attr
                if suffix:
                    new_suffix += '.' + suffix
                return self.attr_to_name(node.value, new_suffix)
            return suffix

        def visit_Call(self, stmt):
            name = None
            if isinstance(stmt.func, ast.Name):
                name = stmt.func.id
            if isinstance(stmt.func, ast.Attribute):
                name = self.attr_to_name(stmt.func)
            if name is not None and name:
                self.parent.calls.append(name)
            self.continue_parsing(stmt)

        def visit_ClassDef(self, stmt):
            self.parent.class_names.append(str(stmt.name))
            self.continue_parsing(stmt)

    # noinspection PyPep8Naming,PyDocstring
    class ExportableParser(ast.NodeVisitor):
        """sets parent.class_names, parent.function_names, parent.variable_names"""

        def __init__(self, parent):
            self.parent = parent

        def continue_parsing(self, stmt):
            """
            Helper: parse a node's children

            :param stmt: AST statement
            """
            super(ModuleInfo.ExportableParser, self).generic_visit(stmt)

        def visit_ClassDef(self, stmt):
            # self.parent.class_names.append(str(stmt.name))
            for class_stmt in stmt.body:
                if isinstance(class_stmt, ast.Assign):
                    for target in class_stmt.targets:
                        if isinstance(target, ast.Name):
                            self.parent.variable_names.append(stmt.name + '.' + target.id)
            # self.continue_parsing(stmt)

        def visit_FunctionDef(self, stmt):
            self.parent.function_names.append(str(stmt.name))
            # self.continue_parsing(stmt)

        def visit_Module(self, stmt):
            for module_stmt in stmt.body:
                if isinstance(module_stmt, ast.Assign):
                    for target in module_stmt.targets:
                        if isinstance(target, ast.Name):
                            self.parent.variable_names.append(target.id)
            # self.continue_parsing(stmt)
