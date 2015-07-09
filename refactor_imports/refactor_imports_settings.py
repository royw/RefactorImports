# coding=utf-8
"""
RefactorImportsSettings adds application specific information to the generic ApplicationSettings class.
"""
import os
from refactor_imports.utils.application_settings import ApplicationSettings

__docformat__ = 'restructuredtext en'
__all__ = ("RefactorImportsSettings",)


class RefactorImportsSettings(ApplicationSettings):
    """
    Usage::

        with RefactorImportsSettings() as settings:
        try:
            app.execute(self, settings)
            exit(0)
        except ArgumentError as ex:
            error(str(ex))
            exit(1)
    """
    HELP = {
        'RefactorImports': "Refactor imports in python source files.",

        'options_group': '',
        'top_dir': 'The directory that contains the package directories to refactor. (default=".")',
        'all': 'List imports for all the objects in the package hierarchy',
        'usages': 'List usages of package.module.* symbols',
        'imports': 'List the desired import lines for each module.',
        'dump': 'Dump AST tree for each module',

        'info_group': '',
        'version': "Show RefactorImports's version.",
        'longhelp': 'Long help about RefactorImports.',

        'output_group': 'Options that control generated output.',
        'verbosity': 'Set verbosity level: 0=none, 1=errors, 2=info+errors, 3+=debug+info+errors (default=2).',
        'logfile': 'File to log all messages (debug, info, warning, error, fatal) to.',
    }

    def __init__(self):
        super(RefactorImportsSettings, self).__init__('RefactorImports', 'refactor_imports', ['RefactorImports'], self.HELP)

    def _cli_options(self, parser):
        """
        Adds application specific arguments to the parser.

        :param parser: the argument parser with --conf_file already added.
        :type parser: argparse.ArgumentParser
        """
        options_group = parser.add_argument_group(title='Options', description=self._help['options_group'])
        options_group.add_argument('--top_dir', type=str, metavar='DIR', default=os.path.curdir,
                                   help=self._help['top_dir'])
        options_group.add_argument('--all', action='store_true', help=self._help['all'])
        options_group.add_argument('--usages', action='store_true', help=self._help['usages'])
        options_group.add_argument('--imports', action='store_true', help=self._help['imports'])
        options_group.add_argument('--dump', action='store_true', help=self._help['dump'])

        info_group = parser.add_argument_group(title='Informational Commands', description=self._help['info_group'])
        info_group.add_argument('--version', dest='version', action='store_true', help=self._help['version'])
        info_group.add_argument('--longhelp', dest='longhelp', action='store_true', help=self._help['longhelp'])

        output_group = parser.add_argument_group(title='Output Options', description=self._help['output_group'])
        output_group.add_argument('--verbosity', dest='verbosity', default=2, type=int, metavar='INT',
                                  help=self._help['verbosity'])
        output_group.add_argument('--logfile', type=str, metavar='FILE', help=self._help['logfile'])

    def _cli_validate(self, settings):
        """
        Verify we have required options for commands.

        :param settings: the settings object returned by ArgumentParser.parse_args()
        :type settings: argparse.Namespace
        :return: the error message if any
        :rtype: str or None
        """
        return None
