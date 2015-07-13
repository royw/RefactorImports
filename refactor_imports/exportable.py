# coding=utf-8

"""
Symbols in a module that other modules may import are referred to here as "Exportable".
This is a wrapper for exportable symbols with basic comparison and conversions.
"""

from refactor_imports.utils.comparable_mixin import ComparableMixin

__author__ = 'roy'


class Exportable(ComparableMixin):
    """
    Usage::

        exportable = Exportable("refactor_imports.exportable", "exportable.py", "Exportable")
        print(str(exportable))
        print(exportable.import_str)
    """

    def __init__(self, module_spec, file_spec, name):
        """
        Exportable(module_spec, file_spec, name)

        :param module_spec: the module_spec which is the concatenation of the package and module name.
        :type module_spec: str
        :param file_spec: the path to the module file
        :type file_spec: str
        :param name: the symbol in the module visible to external modules
        :type name: str
        """
        self.module_spec = module_spec.split('.__init__')[0]
        self.file_spec = file_spec
        self.name = name
        self.full_name = '.'.join([module_spec, name])

    def __str__(self):
        return "{module}.{name}".format(module=self.module_spec, name=self.name)

    @property
    def import_str(self):
        """
        :return: a string that may be used to import this exportable
        :rtype: str
        """
        return "from {module} import {name}".format(module=self.module_spec, name=self.name)

    def _cmpkey(self):
        return self.full_name
