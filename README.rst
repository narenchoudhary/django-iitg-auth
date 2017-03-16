django-iitg-auth
================

``django-iitg-auth`` is a reusable Django application which provides
a custom authencation backend for authenticating with IIT Guwahati webmail servers,
a login form and a utility view.

Installation
============

``django-iitg-auth`` can be installed using following pip command.

.. code-block:: python

    pip install git+https://github.com/narenchoudhary/django-iitg-auth#egg=django-iitg-auth


Usage: Authentication Backend
=============================

Add ``'iitgauth'`` to INSTALLED_APPS settings of the project.

.. code-block:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        ...
        ...
        'iitgauth',
    ]

Add ``'iitgauth.auth.WebMailAuthenticationBackend'`` to ``AUTHENTICATION_BACKENDS`` in settings.py.

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'iitgauth.auth.WebMailAuthenticationBackend',
    ]


This is all the configuration required to use the webmail authentication backend.


Note that ``authenticate`` method of the backend requires following credentials:
    * username
    * password
    * login server
    * port (default is set to 995)

Following snippet shows how webmail authentication can be done in a custom view.

.. code-block:: python

    from django.contrib.auth import authenticate
    from django.views.generic import View

    class LoginView(View):

        def get(self, request):
            # get request handling logic
            #

        def post(self, request):
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data('username')
                password = form.cleaned_data('password')
                login_server = form.cleaned_data('login_server')

                # open a socket to login server and query validity of credentials
                user = auth.authenticate(username=username, password=password,
                            login_server=login_server, port=995)
                #
                # rest of authentication logic
                #
           else:
               # invalid form hadling


Usage: ``WebmailLoginForm`` and ``WebmailLoginView``
====================================================
A ready-to-use form (``WebmailLoginForm``) and a class based view (``WebmailLoginView``) are also available.
Using this form and view is not necessary. You can write your own custom login form and view to use with
webmail authentication backend as explained above.

This form works exactly similar to Django's built-in AuthenticationForm_.
Only difference is ``WebmailLoginForm`` has one extra field, .i.e. Login Server field.

``WebmailLoginForm`` has 3 fields:
    * username
    * password
    * login_server

.. _AuthenticationForm: https://docs.djangoproject.com/en/1.10/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm


``WebmailLoginView`` is a FormView_ which renders ``WebmailLoginForm`` on GET and redirects to ``success_url`` on successful authentication.

.. _FormView: https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-editing/#formview


Demo
====

**Note:** There is a working demo project available under **example** directory.
