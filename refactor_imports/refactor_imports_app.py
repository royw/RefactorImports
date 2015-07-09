# coding=utf-8
"""
The RefactorImports application.

"""
from refactor_imports.utils.graceful_interrupt_handler import GracefulInterruptHandler
from refactor_imports.utils.simple_logger import Logger, FileLogger
from refactor_imports.code_analyzer import CodeAnalyzer
from refactor_imports.utils.list_helper import unique_list

__docformat__ = 'restructuredtext en'
__all__ = ("RefactorImportsApp",)


# noinspection PyMethodMayBeStatic
class RefactorImportsApp(object):
    """
    This is the application class.

    Usage::

        cli = RefactorImportsCLI()
        cli.execute(RefactorImportsApp())

    """

    def __init__(self):
        """
        The CodeAnalyzer application.
        """
        # noinspection PyArgumentEqualDefault
        Logger.set_verbose(True)
        Logger.set_debug(False)

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    def execute(self, settings):
        """
        Execute the tasks specified in the settings object.

        :param settings: the application settings
        :type settings: argparse.Namespace
        :return: None
        :raises: ArgumentError
        """
        Logger.set_verbosity(settings.verbosity)
        if settings.logfile is not None and settings.logfile:
            Logger.add_logger(FileLogger(settings.logfile))

        with GracefulInterruptHandler() as handler:
            analyzer = CodeAnalyzer(settings.top_dir)
            if settings.dump:
                for module in analyzer.find_modules(settings.top_dir):
                    print("{name}:".format(name=module.file_spec))
                    print(module.dump_tree())
                    print("\n")

            exportables = analyzer.exportables()
            if settings.all:
                for exportable in exportables:
                    print(exportable.import_str)

            if settings.usages:
                calls = analyzer.calls()
                for module_name in sorted(calls.keys()):
                    print("{module}:".format(module=module_name))
                    for call in calls[module_name]:
                        print("  " + call)
