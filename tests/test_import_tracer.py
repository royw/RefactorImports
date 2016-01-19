# coding=utf-8

"""
Test the ImportTracer
"""
import os

import sys

from refactor_imports.code_analyzer import CodeAnalyzer
from refactor_imports.import_tracer import ImportTracer

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'

# top_dir = os.path.join(os.path.dirname(__file__), 'data')
top_dir = os.path.dirname(__file__)

sys.path.append(top_dir)


def test_against_files():
    """
    test that all data modules that start with the lowercase letter 'p' generate a patch,
    while all others do not generate a patch.
    """
    analyzer = CodeAnalyzer(top_dir)
    for module in analyzer.find_modules(top_dir):
        print("\n" + module.module_spec)
        print(module.file_spec)
        tracer = ImportTracer(module_spec=module.module_spec, file_spec=module.file_spec)
        patch = tracer.execute()
        if os.path.basename(str(module.file_spec)).startswith('p'):
            assert patch
            print(patch)
        else:
            assert not patch


def test_pprint_import():
    """
    Test that all names from pprint get imported into p1.py
    """
    analyzer = CodeAnalyzer(top_dir)
    for module in analyzer.find_modules(top_dir):
        if os.path.basename(module.file_spec) == 'p1.py':
            print("\n" + module.module_spec)
            print(module.file_spec)
            tracer = ImportTracer(module_spec=module.module_spec, file_spec=module.file_spec)
            patch = tracer.execute()
            assert patch
            print(patch)
            for name in ['pformat', 'pprint', 'saferepr', 'isreadable', 'PrettyPrinter', 'isrecursive']:
                assert "+from pprint import {name}".format(name=name) in patch


def test_importing_same_name():
    """
    test that two adjacent wildcard imports where each module defines a common name, both generate
    explicit imports for the common name.  i.e.:

        from t3 import *
        from t4 import *

    becomes:

        from t3 import Bar
        from t3 import Charlie
        from t4 import Bar
        from t4 import Delta
    """
    analyzer = CodeAnalyzer(top_dir)
    for module in analyzer.find_modules(top_dir):
        if os.path.basename(module.file_spec) == 'p2.py':
            print("\n" + module.module_spec)
            print(module.file_spec)
            tracer = ImportTracer(module_spec=module.module_spec, file_spec=module.file_spec)
            patch = tracer.execute()
            assert "-from data.t3 import *" in patch
            assert "+from data.t3 import Bar" in patch
            assert "+from data.t3 import Charlie" in patch
            assert "-from data.t4 import *" in patch
            assert "+from data.t4 import Bar" in patch
            assert "+from data.t4 import Delta" in patch
