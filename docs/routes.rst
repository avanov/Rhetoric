Route Pattern Syntax
--------------------

.. note:: This section is copied from
   `Pyramid Docs <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-pattern-syntax>`_,
   since Rhetoric provides the same pattern matching functionality.

The *pattern* used in route configuration may start with a slash character.
If the pattern does not start with a slash character, an implicit slash will
be prepended to it at matching time.  For example, the following patterns are
equivalent:

.. code-block:: text

   {foo}/bar/baz

and:

.. code-block:: text

   /{foo}/bar/baz

A pattern segment (an individual item between ``/`` characters in the
pattern) may either be a literal string (e.g. ``foo``) *or* it may be a
replacement marker (e.g. ``{foo}``) or a certain combination of both. A
replacement marker does not need to be preceded by a ``/`` character.

A replacement marker is in the format ``{name}``, where this means "accept
any characters up to the next slash character and use this as the input parameter
for a view callable.

A replacement marker in a pattern must begin with an uppercase or lowercase
ASCII letter or an underscore, and can be composed only of uppercase or
lowercase ASCII letters, underscores, and numbers.  For example: ``a``,
``a_b``, ``_b``, and ``b9`` are all valid replacement marker names, but
``0a`` is not.

A matchdict is the dictionary representing the dynamic parts extracted from a
URL based on the routing pattern.  It is available as ``request.matchdict``.
For example, the following pattern defines one literal segment (``foo``) and
two replacement markers (``baz``, and ``bar``):

.. code-block:: text

   foo/{baz}/{bar}

The above pattern will match these URLs, generating the following matchdicts:

.. code-block:: text

   foo/1/2        -> {'baz':u'1', 'bar':u'2'}
   foo/abc/def    -> {'baz':u'abc', 'bar':u'def'}

It will not match the following patterns however:

.. code-block:: text

   foo/1/2/        -> No match (trailing slash)
   bar/abc/def     -> First segment literal mismatch

Replacement markers can optionally specify a regular expression which will be
used to decide whether a path segment should match the marker.  To specify
that a replacement marker should match only a specific set of characters as
defined by a regular expression, you must use a slightly extended form of
replacement marker syntax.  Within braces, the replacement marker name must
be followed by a colon, then directly thereafter, the regular expression.
The *default* regular expression associated with a replacement marker
``[^/]+`` matches one or more characters which are not a slash.  For example,
under the hood, the replacement marker ``{foo}`` can more verbosely be
spelled as ``{foo:[^/]+}``.  You can change this to be an arbitrary regular
expression to match an arbitrary sequence of characters, such as
``{foo:\d+}`` to match only digits.

It is possible to use two replacement markers without any literal characters
between them, for instance ``/{foo}{bar}``. However, this would be a
nonsensical pattern without specifying a custom regular expression to
restrict what each marker captures.

Segments must contain at least one character in order to match a segment
replacement marker.  For example, for the URL ``/abc/``:

- ``/abc/{foo}`` will not match.

- ``/{foo}/`` will match.
