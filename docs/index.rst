====================
Rhetoric
====================

.. image:: https://pypip.in/v/Rhetoric/badge.png
        :target: https://crate.io/packages/Rhetoric

.. image:: https://pypip.in/d/Rhetoric/badge.png
        :target: https://crate.io/packages/Rhetoric

.. image:: https://api.travis-ci.org/avanov/Rhetoric.png
        :target: https://travis-ci.org/avanov/Rhetoric

.. image:: https://coveralls.io/repos/avanov/Rhetoric/badge.png?branch=develop
        :target: https://coveralls.io/r/avanov/Rhetoric?branch=develop

Status: **Beta, Unstable API**.

Naive implementation of Pyramid-like routes for Django projects.


Why it is worth your while
==========================

There's a great article on why Pyramid routing subsystem is so convenient for
web developers -
`Pyramid view configuration: Let me count the ways <http://blog.delaguardia.com.mx/pyramid-view-configuration-let-me-count-the-ways.html>`_.

As a person who uses Pyramid as a foundation for his pet-projects, and Django - at work,
I (the author) had a good opportunity to compare two different approaches to routing configuration
provided by these frameworks. And I totally agree with the key points of the article - Pyramid routes
are more flexible and convenient for developers writing RESTful services.

The lack of flexibility of standard Django url dispatcher motivated me to
create this project. I hope it will be useful for you,
and if you liked the idea behind Rhetoric URL Dispatcher, please consider
`Pyramid Web Framework <http://www.pylonsproject.org/>`_ for one of your future projects.


Project premises
================

* Rhetoric components try to follow corresponding Pyramid components whenever possible.
* Integration with django applications shall be transparent to existing code whenever possible.
* Performance of Rhetoric URL Dispatcher is worse than of the one of Pyramid, due to
  naivety of the implementation and limitations imposed by the compatibility with Django API.

Installation
=============

Rhetoric is available as a PyPI package:

.. code-block:: bash

    $ pip install Rhetoric

The package shall be compatible with Python2.7, and Python3.3 or higher.

Integration with Django
=======================

#. Replace ``django.middleware.csrf.CsrfViewMiddleware`` with
   ``rhetoric.middleware.CsrfProtectedViewDispatchMiddleware`` in your project's ``MIDDLEWARE_CLASSES``:

   .. code-block:: python
      :linenos:

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
      :linenos:

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
          re.compile('^project_name.settings[_]?[_a-z09]*$').match,
      ])
      urlpatterns.extend(config.django_urls())

#. Register views:

   .. code-block:: python
      :linenos:

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
====================

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


View Configuration Parameters
==============================

.. note:: This section is partly copied from the
   `Pyramid documentation <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#view-configuration-parameters>`_,
   since Rhetoric provides almost the same functionality.


Non-Predicate Arguments
-----------------------

``renderer``

Predicate Arguments
-----------------------

``route_name``

``request_method``

``api_version``

    .. versionadded:: 0.1.7

    Available patterns:




Renderers
===========================

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


Varying Attributes of Rendered Responses
----------------------------------------

.. note:: This section is partly copied from the
   `Pyramid Renderers documentation <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html#varying-attributes-of-rendered-responses>`_,
   since Rhetoric provides almost the same API.

.. versionadded:: 0.1.8

Before a response constructed by a :term:`renderer` is returned to
``Django``, several attributes of the request are examined which have the
potential to influence response behavior.

View callables that don't directly return a response should use the API of
the :class:`django.http.HttpResponse` attribute available as
``request.response`` during their execution, to influence associated response
behavior.

For example, if you need to change the response status from within a view
callable that uses a renderer, assign the ``status_code`` attribute to the
``response`` attribute of the request before returning a result:

.. code-block:: python
   :linenos:

   from rhetoric import view_config

   @view_config(name='dashboard', renderer='dashboard.html')
   def myview(request):
       request.response.status_code = 404
       return {'URL': request.get_full_path()}

Note that mutations of ``request.response`` in views which return a HttpResponse
object directly will have no effect unless the response object returned *is*
``request.response``.  For example, the following example calls
``request.response.set_cookie``, but this call will have no effect, because a
different Response object is returned.

.. code-block:: python
   :linenos:

   from django.http import HttpResponse

   def view(request):
       request.response.set_cookie('abc', '123') # this has no effect
       return HttpResponse('OK') # because we're returning a different response

If you mutate ``request.response`` and you'd like the mutations to have an
effect, you must return ``request.response``:

.. code-block:: python
   :linenos:

   def view(request):
       request.response.set_cookie('abc', '123')
       return request.response


Request properties
------------------

``request.json_body`` - http://docs.pylonsproject.org/projects/pyramid/en/latest/api/request.html#pyramid.request.Request.json_body


Predicates
==========

request_method
~~~~~~~~~~~~~~

api_version
~~~~~~~~~~~


@view_defaults Class Decorator
==============================

.. note:: This section is copied from
   `Pyramid Docs <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#view-defaults-class-decorator>`_,
   since Rhetoric provides the same functionality.

.. versionadded:: 0.1.7


If you use a class as a view, you can use the
:class:`rhetoric.view.view_defaults` class decorator on the class to provide
defaults to the view configuration information used by every ``@view_config``
decorator that decorates a method of that class.

For instance, if you've got a class that has methods that represent "REST
actions", all which are mapped to the same route, but different request
methods, instead of this:

.. code-block:: python
   :linenos:

   from rhetoric import view_config

   class RESTView(object):
       def __init__(self, request, *args, **kw):
           self.request = request

       @view_config(route_name='rest', request_method='GET', renderer='json')
       def get(self):
           return {'method': 'GET'}

       @view_config(route_name='rest', request_method='POST', renderer='json')
       def post(self):
           return {'method': 'POST'}

       @view_config(route_name='rest', request_method='DELETE', renderer='json')
       def delete(self):
           return {'method': 'DELETE'}

You can do this:

.. code-block:: python
   :linenos:

   from rhetoric import view_config
   from rhetoric import view_defaults

   @view_defaults(route_name='rest', renderer='json')
   class RESTView(object):
       def __init__(self, request, *args, **kw):
           self.request = request

       @view_config(request_method='GET')
       def get(self):
           return {'method': 'GET'}

       @view_config(request_method='POST')
       def post(self):
           return {'method': 'POST'}

       @view_config(request_method='DELETE')
       def delete(self):
           return {'method': 'DELETE'}

In the above example, we were able to take the ``route_name='rest'`` and
``renderer='json'`` arguments out of the call to each individual ``@view_config``
statement, because we used a ``@view_defaults`` class decorator to provide
the argument as a default to each view method it possessed.

Arguments passed to ``@view_config`` will override any default passed to
``@view_defaults``.

ADT
======

ADT stands for Algebraic Data Type.

.. code-block:: python

    # --------------------------
    # project/payments/models.py
    # --------------------------
    from rhetoric.adt import adt


    # Declare a new ADT
    class PaymentMethod(adt):
        # Define variants in a form of VARIANT_NAME = variant_value
        PAYPAL = 'paypal'
        CHEQUE = 'cheque'
        DATACASH = 'bank_transfer'
        ## uncomment the following variant and you will get a configuration error like:
        ##     "Case payment_processor of PaymentMethod is not exhaustive.
        ##      Here is the variant that is not matched: GOOGLE_CHECKOUT"
        ## You will have to implement a payment processor case (see below)
        ## for the GOOGLE_CHECKOUT variant in order to fix the error.
        #GOOGLE_CHECKOUT = 'google_checkout'


    # -------------------------
    # project/payments/logic.py
    # -------------------------
    from project.payments.models import PaymentMethod

    @PaymentMethod('PAYPAL', 'payment_processor')
    def process_paypal():
        pass

    @PaymentMethod('CHEQUE', 'payment_processor')
    def process_cheque():
        pass

    @PaymentMethod('DATACASH', 'payment_processor')
    def process_datacash():
        pass

    # -------------------------------------------
    # Here's the essence of ADT Consistency Check
    # -------------------------------------------
    ## - Uncomment the following definition and you will get a configuration error like:
    ## -    "Variant DATACASH of PaymentMethod is already bound to the case payment_processor: process_datacash"
    ## -
    ## - You cannot bind variants twice within one case.
    ##
    #@PaymentMethod('DATACASH', 'payment_processor')
    #def process_datacash_error():
    #    pass

    ## - Uncomment the following definition and you will get a configuration error like:
    ## -    "Variant AMAZON does not belong to the type PaymentMethod."
    ## -
    ## - You will have to add the AMAZON case to the PaymentMethod ADT in order to fix the error.
    ##
    #@PaymentMethod('AMAZON', 'payment_processor')
    #def process_amazon():
    #    pass

    ## - Uncomment the following definition and you will get a configuration error like:
    ## -     "Case withdraw_form of PaymentMethod is not exhaustive.
    ## -      Here is the variant that is not matched: CHEQUE."
    ## -
    ## - You will have to implement withdraw forms for all other variants - CHEQUE, DATACASH
    ## - in order to fix the error.
    ##
    #@PaymentMethod('PAYPAL', 'withdraw_form')
    #class PaypalWitdrawForm(object):
    #    pass
    #

    # ------------------------------------------------------
    # Here's the essence of ADT from developer's perspective
    # (note the absence of conditional statements such as
    #  if:/elif:/elif:/.../else: raise NotImplementedError()
    # )
    # ------------------------------------------------------

    # ----------------------------
    # project/payments/__init__.py
    # ----------------------------
    from project.payments.models import PaymentMethod

    def includeme(config):
        RULES = {
            'engine': PaymentMethod
        }
        # The {engine} placeholder will be replaced with the (?:paypal|cheque|bank_transfer) regex.
        # Note that here we use the same ADT object, that was previously used for defining
        # cases payment_processor and withdraw_form.
        config.add_route('payments.withdraw', '/payments/withdraw/{engine}', rules=RULES)

    # -------------------------
    # project/payments/views.py
    # -------------------------
    from rhetoric.view import view_config, view_defaults


    @view_defaults(route_name='payments.withdraw', renderer='json')
    class PaymentsHandler(object)
        def __init__(self, request, engine):
            self.request = request
            self.engine = engine
            # Note that we will ALWAYS have a proper match here, because this handler
            # will be reached with only correct HTTP requests
            # (i.e. engine value is one of the variant values of PaymentMethod).
            self.payment_strategy = PaymentMethod.match(engine)

        @view_config(request_method='GET', renderer='payments/withdraw_form.html')
        def show_withdraw_form(self):
            # Here, ``payment_strategy.withdraw_form`` is one of case implementations
            # that we defined above with @PaymentMethod(VARIANT, 'withdraw_form').
            # It always points to the relevant implementation!
            form = self.payment_strategy.withdraw_form
            # Render html form
            return {'form': form}

        @view_config(request_method)
        def process_payment(request_method='POST'):
            # Here, ``payment_strategy.payment_processor`` is one of case implementations
            # that we defined above with @PaymentMethod(VARIANT, 'payment_processor').
            # It always points to the relevant implementation!
            processor = self.payment_strategy.payment_processor
            processor()
            # Render json response
            return {'ok': True, 'message': 'Success.'}




Sources
============

Rhetoric is licensed under `the MIT License <http://opensource.org/licenses/MIT>`_.

We use GitHub as a primary code repository - https://github.com/avanov/Rhetoric

.. include:: ../AUTHORS

.. include:: ../CHANGES


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
