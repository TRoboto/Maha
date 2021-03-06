=================
Adding Docstrings
=================

A docstring is a string literal that is used right after the definition
of a module, function, class, or method. They are used to document our code.
This page will give you a set of guidelines to write efficient and correct docstrings.


Formatting the Docstrings
-------------------------

Please begin the description of the class/function in the same line as
the 3 quotes:

.. code:: py

    def do_this():
        """This is correct.
        (...)
        """


    def dont_do_this():
        """
        This is incorrect.
        (...)
        """

NumPy Format
------------
Maha uses numpy format for the documentation.

Use the numpy format for sections and formatting - see
https://numpydoc.readthedocs.io/en/latest/format.html.

This includes:

#. The usage of ``Attributes`` to specify ALL ATTRIBUTES that a
   class can have and a brief (or long, if
   needed) description.

#. The usage of ``Parameters`` on functions to specify how
   every parameter works and what it does. This should be excluded if
   the function has no parameters. Note that you **should not** specify
   the default value of the parameter on the type. On the documentation
   render, this is already specified on the function's signature. If you
   need to indicate a further consequence of value omission or simply
   want to specify it on the docs, make sure to **specify it in the
   parameter's DESCRIPTION**.

   .. note::
        ``__init__`` parameters should be specified as ``Parameters``
        **on the class docstring**, rather than under ``__init__``.

#. The usage of ``Returns`` to indicate what is the type of a
   function's return value and what exactly it returns (i.e., a brief -
   or long, if needed - description of what this function returns). Can
   be omitted if the function does not explicitly return (i.e., always
   returns ``None`` because ``return`` is never specified, and it is
   very clear why this function does not return at all). In all other
   cases, it should be specified.

#. The usage of ``Examples`` in order to specify an example of usage of
   a function **is highly encouraged** and, in general, should be
   specified for *every function* unless its usage is **extremely
   obvious**, which can be debatable. Even if it is, it's always a good
   idea to add an example in order to give a better orientation to the
   documentation user. Use the following format for Python code:

   .. code:: rst

       .. code:: pycon

            # python code here

#. The usage of ``Raises`` to indicate any exceptions that a function
   may raises. This should be omitted if the function does not raise
   any exceptions.

Make sure to be as explicit as possible in your documentation. We all
want the users to have an easier time using this library.

See :func:`~.keep`, :func:`~.remove`, :func:`~.contains` for examples.

