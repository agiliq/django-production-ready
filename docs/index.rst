.. django-production-ready documentation master file, created by
   sphinx-quickstart on Sat Sep  5 18:34:15 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-production-ready's documentation!
===================================================

django-production-ready is a library to check if your project is production ready or not. eg: If settings.DEBUG is True, then your project is not production ready.

This library is meant to make **minimal** set of checks before you deploy to production. Passing the checks means that your project **may be** production ready, but failing almost certainly means the project **is not** production ready.

Installation
------------

Install the app

    pip install django-production-ready

Add app to settings.INSTALLED_APPS

    INSTALLED_APPS += ('prodready',)


Basic usage
-----------

    python manage.py is_it_ready


Checks
------

This librarys checks following things.

* settings.DEBUG must be False
* settings.TEMPLATE_DEBUG must be False
* settings.DEBUG_PROPAGATE_EXCEPTIONS must be False
* settings.ADMINS and settings.MANAGERS must not be empty
* settings.EMAIL_HOST_USER must not be empty string
* settings.SERVER_EMAIL and settings.DEFAULT_FROM_EMAIL must be changed from Django provided default values.
* 404.html and 500.html must be configured properly
* There must not be any *print* statement in the project
* There must not be any *pdb* or *ipdb* statement in the project

In case of any failed check, management command **is_it_ready** will show a log of failed checks. In such case you should consider your project not ready for production.

Output
------

If all checks pass, you would see::

    --------------------
    Production ready: Yes
    --------------------

If any check fails, you would see log of failed checks. Assuming settings.DEBUG is True, then you would see something like::

    --------------------
    Production ready: No
    --------------------
    Possible errors:
        * Set DEBUG to False


.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`search`
