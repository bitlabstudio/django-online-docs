"""Tests for the views of the ``online_docs`` app."""
import os

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
        self.assertEqual(resp.status_code, 200)

    def test_get_document_name(self):
        req = RequestFactory().get(self.get_url() + '?path=/docs/')
        view = OnlineDocsView()
        view.dispatch(req)
        result = view.get_document_name()
        self.assertEqual(result, 'online_docs_view.md', msg=(
            'Should resolve the given path and return the filename with the'
            ' format "<namespace>.<view_name>.md", but returned %s' % result))

    def test_get_document_file_path(self):
        req = RequestFactory().get(self.get_url() + '?path=/docs/')
        view = OnlineDocsView()
        view.dispatch(req)
        document_name = 'foo_bar.md'
        result = view.get_document_file_path(document_name)
        self.assertEqual(result, os.path.join(
            settings.STATIC_ROOT, 'online_docs', document_name), msg=(
                'Should append the given filename to STATIC_ROOT/online_docs'
                ' but returned %s' % result))

    def test_get_document_content(self):
        req = RequestFactory().get(self.get_url() + '?path=/docs/')
        view = OnlineDocsView()
        view.dispatch(req)
        result = view.get_document_content('foobar.md')
        self.assertEqual(result, None, msg=(
            'Should return None if the given file could not be read'))
