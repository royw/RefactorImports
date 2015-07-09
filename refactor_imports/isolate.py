"""
Facilitate running a code block in s separate process
"""
__author__ = 'roy'

class Isoloate(object):
    """
    with Isoloate().fork as proc:
        dosomething()
    """

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fork(self):
        pass
