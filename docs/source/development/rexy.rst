====
Rexy
====

:mod:`Rexy <maha.rexy>` offers an interface for common regular expression patterns. It builds
few core modules on top of regular expressions. These modules are briefly described here.

See :mod:`Rexy Functions <maha.rexy.rexy>`.

Expression
----------

:class:`~.Expression` is a simple wrapper around a regular expression. It adds pickling
functionality to the compiled regular expression. This speeds up the compilation process of
the sophisticated regular expressions by loading the pickled compiled regular expression.
The compilation speed may increase by a factor of 100x or even more for expressions
like :data:`~.RULE_DURATION`.

.. seealso::
    :meth:`.Expression.compile`, :meth:`.Expression.match`, :meth:`.Expression.search`,
    :meth:`.Expression.fullmatch`, :meth:`.Expression.sub`, :meth:`.Expression.parse`,


Expression Group
----------------

:class:`~.ExpressionGroup` is intended to group multiple :class:`~.Expression` s and to
allow using them as a single regular expression. It also provides a few additional
useful methods. See :meth:`.ExpressionGroup.get_matched_expression` and
:meth:`.ExpressionGroup.smart_parse`.

.. seealso::
    :meth:`.ExpressionGroup.add` and :meth:`.ExpressionGroup.join`


Expression Result
-----------------

:class:`~.ExpressionResult` is an interface for the result of a regular expression match.
It ensures that each parsed result has at least ``start``, ``end``, ``value`` and
``expression`` attributes.
