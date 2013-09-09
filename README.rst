Rhetoric
=============

.. image:: https://pypip.in/v/Rhetoric/badge.png
        :target: https://crate.io/packages/Rhetoric

.. image:: https://pypip.in/d/Rhetoric/badge.png
        :target: https://crate.io/packages/Rhetoric

Status: **Early Development, Unstable API**.

Naive implementation of Pyramid-like routes for Django projects.


Why is it worth your while?
---------------------------

There's a great article on why Pyramid routing subsystem is so convenient for
web developers -
`Pyramid view configuration: Let me count the ways <http://blog.delaguardia.com.mx/pyramid-view-configuration-let-me-count-the-ways.html>`_.

As a person who uses Pyramid as a foundation for his pet-projects, and Django - at work,
I (the author) had a good opportunity to compare two different approaches to routing configuration
provided by these frameworks. And I totally agree with the key points of the article - Pyramid routes
are more flexible and convenient for developers writing RESTful services.

The lack of flexibility of standard Django url dispatcher motivated me to
create this project. I hope it will be useful for you, other django developers,
and if you liked the idea behind Rhetoric URL Dispatcher, please consider
`Pyramid Web Framework <http://www.pylonsproject.org/>`_ for one of your future projects.
It has a dozen of features I'd like to see in Django.


Project premises
----------------

* Rhetoric components try to follow corresponding Pyramid components whenever possible.
* Integration with django applications shall be transparent to existing code whenever possible.
* Performance of Rhetoric URL Dispatcher is worse than of the one of Pyramid, due to
  naivety of the implementation and limitations imposed by the compatibility with Django API.

Installation
-------------

Rhetoric is available as a PyPI package:

.. code-block:: bash

    $ pip install Rhetoric

The package shall be compatible with Python2.7, and Python3.3 or higher.

Integration with Django
-----------------------

#. Replace ``django.middleware.csrf.CsrfViewMiddleware`` with
   ``rhetoric.middleware.CsrfProtectedViewDispatchMiddleware`` in your project's ``MIDDLEWARE_CLASSES``:

   .. code-block:: python

        # somewhere in a project_name.settings module

        MIDDLEWARE_CLASSES = [
            # ...
            'rhetoric.middleware.CsrfProtectedViewDispatchMiddleware',
            #'django.middleware.csrf.CsrfViewMiddleware',
            # ...
        ]

#. Inside the project's `root urlconf <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-ROOT_URLCONF>`_
   (usually ``project_name.urls``):

   .. code-block:: python

       from django.conf.urls import patterns, include, url
       # ... other imports ...
       from rhetoric import Configurator

       # ... various definitions ...

       urlpatterns = patterns('',
           # ... a number of standard django url definitions ...
       )

       # Rhetorical routing
       # ------------------
       config = Configurator()
       config.add_route('test.new.routes', '/test/new/routes/{param:[a-z]+}')
       config.scan(ignore=[
           # do not scan test modules included into the project tree
           re.compile('^.*[.]?tests[.]?.*$').match,
           # do not scan settings modules
           re.compile('^settings[_]?[_a-z09]*$').match,
       ])
       urlpatterns.extend(config.django_urls())

#. Register views:

   .. code-block:: python

       # project_name.some_app.some_module

       from rhetoric import view_config


       @view_config(route_name="test.new.routes", renderer='json')
       def view_get(request, param):
           return {
               'Hello': param
           }

       @view_config(route_name="test.new.routes", renderer='json', request_method='POST')
       def view_post(request, param):
           return {
               'Hello': 'POST'
           }

#. From this point you can request ``/test/new/routes/<param>`` with different methods.

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


Renderers
------------------

.. note:: This section is copied from the
   `Pyramid Renderers documentation <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html#renderers>`_,
   since Rhetoric provides almost the same rendering functionality.


Built-in renderers
-------------------

``string``: String Renderer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``string`` renderer is a renderer which renders a view callable result to
a string.  If a view callable returns a non-Response object, and the
``string`` renderer is associated in that view's configuration, the result
will be to run the object through the Python ``str`` function to generate a
string.

``json``: JSON Renderer
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``json`` renderer renders view callable results to :term:`JSON`.  By
default, it passes the return value through the ``django.core.serializers.json.DjangoJSONEncoder``,
and wraps the result in a response object.  It also sets
the response content-type to ``application/json``.

Here's an example of a view that returns a dictionary.  Since the ``json``
renderer is specified in the configuration for this view, the view will
render the returned dictionary to a JSON serialization:

.. code-block:: python

   from rhetoric import view_config

   @view_config(renderer='json')
   def hello_world(request):
       return {'content':'Hello!'}

The body of the response returned by such a view will be a string
representing the JSON serialization of the return value:

.. code-block:: json

   {"content": "Hello!"}

``.html``: Django Template Renderer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``.html`` template renderer renders views using the standard Django template language. When
used, the view must return a HttpResponse object or a Python *dictionary*.  The
dictionary items will then be used as the template context objects.
