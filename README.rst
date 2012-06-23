Django Online Documentation
===========================

A Django application for showing user documentation on every page of your
project.

Most big customers request a user documentation in Microsoft Word format. We
thought that this is insane because we develop web applications in an agile way
which means that such a documentation would be outdated almost immediately.
There would also be the issue to send the latest documentation to all users so
we thought why not just include the documentation on the page itself. And why
not make the documentation smart enough to only show the docs about the page
that is currently displayed.

This app resolves the current URL and tries to load a Markdown file for the
currently displayed view in a jQuery modal. The files simply need to be stored
in your app's ``/static/online_docs/`` folders.

Now all you have to do is run ``./manage.py collectstatic`` and this app should
be able to find your documentation files.

Please be aware that this is a first prototype and proof of concept for this
idea. It is very simplistic and probably violates DRY and does not support
i18n. This is on the roadmap, though.

This is how it looks like when you are on the ``/docs/`` page and click at the
``Docs`` navigation link:

.. image:: https://github.com/bitmazk/django-online-docs/raw/master/screenshot.png

Installation
------------

If you want to install the latest stable release from PyPi::

    $ pip install django-online-docs

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-online-docs.git#egg=online_docs

Add ``online_docs`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'online_docs',
    )

Add jQuery and jQuery-ui and ``online_docs.js`` to your ``base.html``.
Furthermore ``online_docs/css/styles.css`` will give you some simple styles for
the output that Markdown generates. You can leave out this stylesheet and just
add the styles to your own main stylesheet if you want::

    <head>
        ...
        <link rel="stylesheet" href="{{ STATIC_URL }}css/libs/ui-lightness/jquery-ui-1.8.16.custom.css">
        <link rel="stylesheet" href="{{ STATIC_URL }}online_docs/css/styles.css">
        ...
    </head>
    <body>
        ...
        <!-- Load these scripts before the closing <body> tag -->
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="{{ STATIC_URL }}js/libs/jquery-1.7.0.min.js"><\/script>')</script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/jquery-ui.min.js"></script>
        <script>window.jQuery || document.write('<script src="{{ STATIC_URL }}js/libs/jquery-ui-1.8.19.min.js"><\/script>')</script>
        <script src="{{ STATIC_URL }}online_docs/js/online_docs.js"></script>
    </body>

Add the link to open the docs to your base.html::

    {% load online_docs_tags %}
    ...
    <ul id="navigation">
        ...
        <li>{% render_docs_link request %}</li>
    </ul>

If you don't like the appearance of the docs link, you can override the
template ``online_docs/online_docs_link.html``.

Usage
-----

Just create a ``/static/online_docs/`` folder in your app that you want to
document. Then place ``.md`` files in that folder. The names of the files should
be of the format ``[namespace_]view_name`` (namespace is optional). Don't
forget to run ``./manage.py collectstatic`` after adding or changing such
files.

If you want to document views of third party apps, just create a
``/static/online_docs`` folder in your project's main static folder and place
the files in there.

If you are unsure about the filename, just run your app, go to the view and
click at the docs link. If you have ``DEBUG=True`` the error message will tell
you the expected filename.

Again: Don't forget to run ``./manage.py collectstatic`` after adding or
changing any ``.md`` file.

Contribution
------------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-online-docs
    $ pip install -r requirements.txt
    $ ./online_docs/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.

Oh and... if you submit patches that make our tests fail, you will be publicly
humiliated on http://travis-ci.org/#!/bitmazk/django-online-docs ;)

If you are making changes that need to be tested in a browser (i.e. to the
CSS or JS files), you might want to setup a Django project, follow the
installation insttructions above, then run ``python setup.py develop``. This
will just place an egg-link to your cloned fork in your project's virtualenv.

Roadmap
-------

* Try to run the markdown files through Django's templating engine to provide
  i18n and url support.
* When DEBUG=True, try to load the files via urrlib, which would allow to test
  the files without running collectstatic all the time.
* Allow to link between different doc files
