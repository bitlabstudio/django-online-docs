"""Tests for the templatetags of the ``online_docs`` app."""
from django.test import TestCase, RequestFactory

from online_docs.templatetags.online_docs_tags import render_docs_link


class RenderDocsTestCase(TestCase):
    """Tests for the ``render_docs`` templatetag."""
    def test_tag(self):
        req = RequestFactory().get('foo')
        render_docs_link(req)
        self.assertTemplateUsed(req, 'online_docs/online_docs_link.html')
