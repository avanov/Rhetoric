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
       config.add_route('test.new.routes', '/test/new/routes')
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
       def view_get(request):
           return {
               'Hello': 'GET'
           }

       @view_config(route_name="test.new.routes", renderer='json', request_method='POST')
       def view_post(request):
           return {
               'Hello': 'POST'
           }

#. From this point you can request ``/test/new/routes`` with different methods.
