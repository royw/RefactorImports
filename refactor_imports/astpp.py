# coding=utf-8
"""
A pretty-printing dump function for the ast module.  The code was copied from
the ast.dump function and modified slightly to pretty-print.

Alex Leone (acleone ~AT~ gmail.com), 2010-01-30
"""

from ast import *
import sys


def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.

    :param node:  AST tree node
    :type node: AstNode
    :param annotate_fields: show names and values for fields
    :type annotate_fields: bool
    :param include_attributes: dump includes line numbers and column offsets
    :type include_attributes: bool
    :param indent: indent output
    :type indent: str
    """
    # noinspection PyProtectedMember
    def _format(node_, level=0):
        if isinstance(node_, AST):
            fields = [(a, _format(b, level)) for a, b in iter_fields(node_)]
            if include_attributes and node_._attributes:
                fields.extend([(a, _format(getattr(node_, a), level))
                               for a in node_._attributes])
            return ''.join([
                node_.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                          if annotate_fields else
                          (b for a, b in fields)),
                ')'])
        elif isinstance(node_, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ',' for x in node_))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node_)

    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)


if __name__ == '__main__':

    for filename in sys.argv[1:]:
        print '=' * 50
        print 'AST tree for', filename
        print '=' * 50
        # noinspection PyArgumentEqualDefault
        f = open(filename, 'r')
        fstr = f.read()
        f.close()
        print dump(parse(fstr, filename=filename), include_attributes=True)
        print
