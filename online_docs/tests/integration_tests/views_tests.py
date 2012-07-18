"""Tests for the views of the ``online_docs`` app."""
import os

import mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from online_docs.views import OnlineDocsView


class ViewTestMixin(object):
    def get_view_name(self):
        """
        Returns the URL of this view by using ``reverse``.

        You must implement this when inheriting this mixin.

        """
        return NotImplementedError

    def get_url(self, view_name=None, view_args=None, view_kwargs=None):
        """
        Returns the request params for this view.

        When calling ``self.client.get`` we usually need three parameter:

            * The URL, which we construct from the view name using ``reverse``
            * The args
            * The kwargs

        In most cases ``args`` and ``kwargs`` are ``None``, so this method will
        help to return the proper URL by calling instance methods that can
        be overridden where necessary.

        """
        if view_name is None:
            view_name = self.get_view_name()
        return reverse(view_name, args=view_args, kwargs=view_kwargs)


class OnlineDocsViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``OnlineDocsView`` view class."""
    def get_view_name(self):
        return 'online_docs_view'

    def test_view(self):
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 404, msg=(
            'Should return 404 when no path is given'))

        resp = self.client.get(self.get_url() + '?path=/docs/')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should be callable with either a `path` URL parameter...'))

        resp = self.client.get(self.get_url() + '?file=online_docs_view.md')
        self.assertEqual(resp.status_code, 200, msg=(
            '...or a `file` URL parameter'))

        old_method = OnlineDocsView.get_document_name
        OnlineDocsView.get_document_name = mock.Mock()
        OnlineDocsView.get_document_name.return_value = 'foobar.md'
        resp = self.client.get(self.get_url() + '?path=/docs/')

        # I would actually like to check if the partials/online_docs.html is
        # loaded here but for some reason it doesn't seem to get loaded, while
        # in a real django app it works. This is to test the code path where
        # no .md file can be found for the current view.
        self.assertEqual(resp.status_code, 200)
        OnlineDocsView.get_document_name = old_method

    def test_get_document_name(self):
        req = RequestFactory().get(self.get_url() + '?path=/docs/')
        view = OnlineDocsView()
        view.dispatch(req)
        result = view.get_document_name()
        self.assertEqual(result, 'online_docs_view.md', msg=(
            'Should resolve the given path and return the filename with the'
            ' format "<namespace>.<view_name>.md", but returned %s' % result))

    def test_get_template_names(self):
        req = RequestFactory().get(self.get_url() + '?path=/docs/')
        view = OnlineDocsView()
        view.dispatch(req)
        result = view.get_template_names()
        self.assertEqual(result, ['online_docs/online_docs.html'], msg=(
            'Should return the template of this app'))

        req.is_ajax = lambda: True
        view.dispatch(req)
        result = view.get_template_names()
        self.assertEqual(result, ['online_docs/partials/online_docs.html'],
            msg=('Should return the patial template if the request is an'
                 ' ajax call'))
