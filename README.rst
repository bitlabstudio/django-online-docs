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
in your app's ``/templates/online_docs/`` folders.

Please be aware that this is a first prototype and proof of concept for this
idea. It is very simplistic and probably violates DRY and does not support
i18n. This is on the roadmap, though.

This is how it looks like when you are on the ``/docs/`` page and click at the
``Docs`` navigation link:

.. image:: https://github.com/bitmazk/django-online-docs/raw/master/screenshot.png

Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django
    pip install markdown

If you want to install the latest stable release from PyPi::

    $ pip install django-online-docs

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-online-docs.git#egg=online_docs

Add ``online_docs`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'online_docs',
    )

Hook this app into your ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^docs/$',
            include('online_docs.urls')),
    )

Download jQuery and jQuery-ui and place it in your ``/static/`` folder. Then
add both libraries and ``online_docs.js`` to your ``base.html``.  Furthermore
``online_docs/css/styles.css`` will give you some simple styles for the output
that Markdown generates. You can leave out this stylesheet and just add the
styles to your own main stylesheet if you want::

    <head>
        ...
        <!-- import the jquery-ui stylesheet here -->
        <link rel="stylesheet" href="{{ STATIC_URL }}online_docs/css/styles.css">
        ...
    </head>
    <body>
        ...
        <!-- Load these scripts before the closing <body> tag -->
        <!-- Import jQuery here -->
        <!-- Import jQuery-ui here -->
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

You can test if everything worked fine by running your site and going to the
URL where you have hooked up this app (i.e. ``/docs/?path=/docs/``).

Usage
-----

Just create a ``/templates/online_docs/`` folder in your app that you want to
document. Then place ``.md`` files in that folder. The names of the files should
be of the format ``[namespace_]view_name`` (namespace is optional).

If you want to document views of third party apps, just create a
``/templates/online_docs`` folder in your project's main static folder and
place the files in there.

If you are unsure about the filename, just run your app, go to the view and
click at the docs link. If you have ``DEBUG=True`` the error message will tell
you the expected filename.

Contribute
----------

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

Check the issue tracker on github for milestones and features to come.
