------------------------
Django Production Ready
------------------------

A simple app with a single management command that checks if your project is 
production ready.

Install
--------

* If you use pip_::

    $ pip install django-production-ready

or

* Checkout the source code from github_ and::

    $ python setup.py install

* Add the app to your `INSTALLED_APPS` in the `settings.py`.

    INSTALLED_APPS = (
    ...
    prodready,
    ...
    )

Usage
------

Run the management command to run the tests:

    $ python manage.py is_it_ready


.. _pip: http://www.pip-installer.org/en/latest/
.. _github: https://github.com/agiliq/django-production-ready
