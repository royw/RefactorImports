import os
from pprint import pprint, pformat
from refactor_imports.module_info import ModuleInfo
from refactor_imports.utils.list_helper import unique_list

__author__ = 'roy'


class CodeAnalyzer(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.module_infos = None

    def exportables(self):
        exportables = []
        module_infos = self.find_modules(self.top_dir)
        for info in module_infos:
            exportables.extend(info.exportables)
        return exportables

    def calls(self):
        calls = {}
        module_infos = self.find_modules(self.top_dir)
        for info in module_infos:
            calls[info.module_spec] = sorted(unique_list(info.calls))
        return calls

    # noinspection PyMethodMayBeStatic
    def find_modules(self, top_dir):
        if self.module_infos is not None:
            return self.module_infos
        module_infos = []
        if os.path.isdir(top_dir):
            # package directory structure
            for dir_name, subdir_list, file_list in os.walk(top_dir):
                # python packages must have a __init__.py file

                if '__init__.py' in file_list:
                    for file_name in [name for name in file_list if name.endswith('.py')]:
                        dir_path = os.path.relpath(dir_name, top_dir)
                        module_spec = os.path.splitext(os.path.join(dir_path, file_name))[0].replace('/', '.')
                        file_spec = os.path.join(os.path.abspath(top_dir), dir_path, file_name)
                        module_infos.append(ModuleInfo(module_spec=module_spec, file_spec=file_spec))
        elif os.path.isfile(top_dir):
            # stand-alone file
            file_spec = os.path.abspath(top_dir)
            module_infos.append(ModuleInfo(module_spec='', file_spec=file_spec))

        self.module_infos = module_infos
        return module_infos

