# coding=utf-8

import ast
import os
from refactor_imports.code_analyzer import CodeAnalyzer
from fullmonty.simple_logger import info

__author__ = 'roy'

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_importing_found_exportables():
    """
    This test gets all of the exportable objects then tries to parse and compile each import statement.
    """
    analyzer = CodeAnalyzer(top_dir)
    exportables = analyzer.exportables()

    for exportable in exportables:
        try:
            tree = ast.parse(exportable.import_str, 'eval')
            compile(tree, '<string>', 'exec')
            info(exportable.import_str)
            assert True, exportable.import_str
        except Exception as ex:
            assert False, exportable.import_str + ' : ' + str(ex)


def test_verify_import_bad_object_test():
    """This test verifies the negative case used in the test_importing_found_exportables() test"""
    import_str = 'from refactor_imports import DoesNotExist'
    try:
        tree = ast.parse(import_str, 'eval')
        compile(tree, '<string>', 'exec')
        info(import_str)
        assert False, import_str
    except Exception as ex:
        assert True, import_str + ' : ' + str(ex)


def test_verify_import_bad_package_test():
    """This test verifies the negative case used in the test_importing_found_exportables() test"""
    import_str = 'from refactor_imports.bad_package import DoesNotExist'
    try:
        tree = ast.parse(import_str, 'eval')
        compile(tree, '<string>', 'exec')
        info(import_str)
        assert False, import_str
    except Exception as ex:
        assert True, import_str + ' : ' + str(ex)
