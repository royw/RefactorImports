# coding=utf-8
"""
Setup for RefactorImports
"""
import os
import re
from setuptools import setup

from sys import version

if version < '2.6':
    print('RefactorImports requires python 2.6 or newer')
    exit(-1)


VERSION_REGEX = r'__version__\s*=\s*[\'\"](\S+)[\'\"]'


def get_project_version():
    """
    Get the version from __init__.py with a line: /^__version__\s*=\s*(\S+)/
    If it doesn't exist try to load it from the VERSION.txt file.
    If still no joy, then return '0.0.0'

    :returns: the version string
    :rtype: str
    """

    # trying __init__.py first
    try:
        file_name = os.path.join(os.getcwd(), 'refactor_imports', '__init__.py')
        # noinspection PyArgumentEqualDefault
        with open(file_name, 'r') as inFile:
            for line in inFile.readlines():
                match = re.match(VERSION_REGEX, line)
                if match:
                    return match.group(1)
    except IOError:
        pass
    # no joy again, so return default
    return '0.0.0'


setup(
    name='RefactorImports',
    version=get_project_version(),
    author='Roy Wright',
    author_email='roy@wright.org',
    url='http://refactor_imports.example.com',
    packages=['refactor_imports'],
    package_dir={'': '.'},
    package_data={'refactor_imports': ['*.txt', '*.js', '*.html', '*.css'],
                  'tests': ['*'],
                  '': ['*.rst', '*.txt', '*.rc', '*.in']},
    license='license.txt',
    description='Refactor imports in python source files.',
    long_description=open('README.rst').read(),
    # use keywords relevant to the application
    keywords=[],
    # use classifiers from:  https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    install_requires=[
        # "argparse",
        # "mako"
        # "Foo >= 1.2.3"
        # 'astpp',
    ],
    entry_points={
        'console_scripts': ['refactor_imports = refactor_imports.refactor_imports_main:main']
    })
