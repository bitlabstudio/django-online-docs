"""Tests for the templatetags of the ``online_docs`` app."""
from mock import Mock, patch

from django.template import Context
from django.template.base import TemplateSyntaxError
from django.test import TestCase, RequestFactory

from online_docs.templatetags.online_docs_tags import (
    URLCrossReferenceNode,
    render_docs_link,
    url_cross_reference,
)


class RenderDocsTestCase(TestCase):
    """Tests for the ``render_docs`` templatetag."""
    def test_tag(self):
        req = RequestFactory().get('foo')
        render_docs_link(req)
        self.assertTemplateUsed(req, 'online_docs/online_docs_link.html')


class URLCrossReferenceTestCase(TestCase):
    """Tests for the ``url_cross_reference`` templatetag."""
    @patch('django.template.Variable')
    def test_tag(self, variable_mock):
        parser = Mock()
        token = Mock(methods=['split_contents'])

        token.split_contents.return_value = (
            'url_cross_reference', 'filename.md', 'link text')
        url = url_cross_reference(parser, token)
        self.assertIsInstance(url, URLCrossReferenceNode, msg=(
            'Should return a URLCrossReferenceNode if called propery'))

        token.split_contents.return_value = (
            'url_cross_reference', 'filename.md', 'link text', 'as', 'var')
        url = url_cross_reference(parser, token)
        self.assertIsInstance(url, URLCrossReferenceNode, msg=(
            'Should return a URLCrossReferenceNode if called propery with'
            ' as var'))

        token.split_contents.return_value = (
            'url_cross_reference', 'filename.md')
        # Should raise an error if no link text argument provided
        self.assertRaises(TemplateSyntaxError, url_cross_reference, parser,
            token)

        token.split_contents.return_value = (
            'url_cross_reference', )
        # Should raise an error if no arguments provided
        self.assertRaises(TemplateSyntaxError, url_cross_reference, parser,
            token)

        token.split_contents.return_value = (
            'url_cross_reference', 'as', 'foobar')
        # Should raise an error if no arguments provided with `as var`
        self.assertRaises(TemplateSyntaxError, url_cross_reference, parser,
            token)

        token.split_contents.return_value = (
            'url_cross_reference', 'filename.md', 'as', 'foobar')
        # Should raise an error if no link text argument provided with `as var`
        self.assertRaises(TemplateSyntaxError, url_cross_reference, parser,
            token)


class URLCrossReferenceNodeTestCase(TestCase):
    """Tests for the ``URLCrossReferenceNode`` class."""
    def test_node(self):
        filename = Mock()
        filename.var = 'filename.md'
        link_text = Mock()
        link_text.var = 'link text'
        ctx = Context({})

        expected = '<a class="onlineDocsLink" href="/docs/?file=filename.md">link text</a>'  #NOQA

        node = URLCrossReferenceNode(filename, link_text, None)
        result = node.render(ctx)
        self.assertEqual(result, expected, msg=(
            'When called with a filename and link name it should return the'
            ' expected link'))

        node = URLCrossReferenceNode(filename, link_text, 'var_name')
        result = node.render(ctx)
        self.assertEqual(ctx['var_name'], expected, msg=(
            'When called with `as var` the context should be updated with'
            ' the result'))
        self.assertEqual(result, '', msg=(
            'When called with `as var` the output should be empty'))
