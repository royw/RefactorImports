from refactor_imports.utils.comparable_mixin import ComparableMixin

__author__ = 'roy'


class Exportable(ComparableMixin):
    def __init__(self, module_spec, file_spec, name):
        self.module_spec = module_spec.split('.__init__')[0]
        self.file_spec = file_spec
        self.name = name
        self.full_name = '.'.join([module_spec, name])

    def __str__(self):
        return "{module}.{name}".format(module=self.module_spec, name=self.name)

    @property
    def import_str(self):
        return "from {module} import {name}".format(module=self.module_spec, name=self.name)

    def _cmpkey(self):
        return self.full_name
