Django Online Documentation
===========================

A Django application for showing user documentation on every page of your
project.

It resolves the current URL and tries to load a Markdown file for the
currently displayed view in a jQuery modal. The files simply need to be stored
in your app's `/static/` folders.

Installation
------------

Do this::

    $ pip install django-online-docs

Add `online_docs` to your `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...,
        'online_docs',
    )

Add jquery and jquery-ui and `online_docs.js` to your `base.html`::

    <head>
        ...
        <link rel="stylesheet" href="{{ STATIC_URL }}css/libs/ui-lightness/jquery-ui-1.8.16.custom.css">
        ...
    </head>
    <body>
        ...
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
template `online_docs/online_docs_link.html`.

Usage
-----

Just place `.md` files in all your apps' static folders. The names of the files
should be of the format `[namespace_]view_name` (namespace is optional). Don't
forget to run `./manage.py collectstatic`.

Roadmap
-------

* Try to run the markdown files through Django's templating engine to provide
  i18n and url support.
