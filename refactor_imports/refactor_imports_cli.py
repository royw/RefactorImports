# coding=utf-8
"""
The command line interface for the RefactorImports application.

"""
__docformat__ = 'restructuredtext en'

from refactor_imports.refactor_imports_settings import RefactorImportsSettings
from refactor_imports.utils.simple_logger import error, info

__all__ = ("ArgumentError", "RefactorImportsCLI")


class ArgumentError(RuntimeError):
    """There is a problem with a command line argument"""
    pass


class RefactorImportsCLI(object):
    """
    Command Line Interface for the CodeAnalyzer App
    """

    def execute(self, app):
        """
        Handle the command line arguments then execute the app.

        :param app: the application instance
        :type app: refactor_imports.RefactorImportsApp
        """
        with RefactorImportsSettings() as settings:
            try:
                results = app.execute(settings)
                if results is not None:
                    self.report(results)
                exit(0)
            except ArgumentError as ex:
                error(str(ex))
                exit(1)

    def report(self, results):
        """

        :param results: (success[], error[], missing_filters_for_rule_ids[])
        :type results: tuple
        """
        # TODO: implement result report
        info("Results: {results}".format(results=repr(results)))
