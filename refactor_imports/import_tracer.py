# coding=utf-8

"""
Describe Me!
"""
import collections
import difflib
import inspect
import multiprocessing
from multiprocessing import Process

import sys

import re
# dictdiffer is in py-dictdiffer
# noinspection PyPackageRequirements
from dictdiffer import DictDiffer
from fullmonty.simple_logger import info, debug, error

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'


# noinspection PyShadowingBuiltins
def flatten(l):
    try:
        # noinspection PyUnboundLocalVariable
        basestring = basestring
    except NameError:
        basestring = (str, bytes)
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el


class ImportTracer(object):
    """
    In a separate process, import a module and capture the locals and globals around each import statement.
    """

    def __init__(self, module_spec, file_spec):
        self.module_spec = module_spec
        self.file_spec = file_spec

    def execute(self):
        # noinspection PyBroadException
        try:
            multiprocessing.set_start_method('spawn')
        except:
            debug('Using default process start method')

        # the module tracer holds content over the entire module
        tracer = ImportTracer.ModuleTracer(self.file_spec)
        q = multiprocessing.Queue()
        p = Process(target=ImportTracer.module_trace, args=(self.module_spec, self.file_spec, tracer, q))
        p.start()
        patch = q.get()
        p.join()
        return patch

    @staticmethod
    def module_trace(module_spec, file_spec, tracer, q):
        """
        Load self.file_path and trace the imports

        :param module_spec: module path
        :type module_spec: str
        :param tracer: tracer context
        :type tracer: ImportTracer.ModuleTracer
        """

        # trace the import of the module
        info("__import__({name})".format(name=module_spec))
        sys.settrace(tracer.trace_imports)
        try:
            __import__(module_spec)
        except ImportError as ex:
            error("Error tracing import.  " + str(ex))
        sys.settrace(None)
        q.put(tracer.to_patch(file_spec))

    class ModuleTracer(object):

        def __init__(self, file_spec):
            self.file_spec = file_spec
            self.diffs = []
            self.last_locals = {}
            self.last_globals = {}

        # noinspection PyUnusedLocal
        def trace_imports(self, frame, event, arg):
            frame_info = inspect.getframeinfo(frame)
            if frame_info[0] == self.file_spec:
                f_globals = dict(frame.f_globals)
                f_globals.pop('__builtins__', None)

                f_locals = dict(frame.f_locals)
                f_locals.pop('__builtins__', None)

                diff = {
                    'added_globals': DictDiffer(f_globals, self.last_globals).added(),
                    'added_locals': DictDiffer(f_locals, self.last_locals).added(),
                    'line_number': frame_info[1],
                    'filename': frame_info[0],
                    'source_line': frame_info[3],
                }
                self.diffs.append(diff)

                if not self.last_locals:
                    self.last_locals = f_locals
                if not self.last_globals:
                    self.last_globals = f_globals

            return self.trace_imports

        def to_patch(self, file_spec):
            # post-process the trace

            # get the source file and make a copy
            with open(file_spec) as source_file:
                original_source = source_file.readlines()
            new_source = original_source[:]

            # process all of the trace diffs.  We want only diffs:
            #
            # * for the current file
            # * whose source line is "from BLAH import *"
            # * and adds symbols to our locals and/or globals

            for index, diff in enumerate(self.diffs):
                try:
                    if diff['filename'] == file_spec:
                        code_context = ''.join(diff['source_line']).strip()
                        match = re.search(r'^\s*from\s+(\S+)\s+import\s+[*]', code_context)
                        if match:
                            # get the added symbols from the union of the locals and globals in the next tracer diff
                            added_symbols = self.diffs[index + 1]['added_locals'] | \
                                            self.diffs[index + 1]['added_globals']
                            if added_symbols:
                                new_lines = []
                                for symbol in added_symbols:
                                    new_lines.append("from {src} import {symbol}\n".format(src=match.group(1),
                                                                                           symbol=symbol))
                                # replace wildcard import with list of explicit imports
                                new_source[diff['line_number'] - 1] = new_lines[:]
                except IndexError:
                    pass

            patch = ''.join(difflib.unified_diff(original_source,
                                                 list(flatten(new_source)),
                                                 fromfile=file_spec,
                                                 tofile=file_spec))
            return patch
