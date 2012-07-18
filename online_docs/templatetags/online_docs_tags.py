"""Templatetags for the ``online_docs`` app."""
from django import template
from django.template.base import TemplateSyntaxError
from django.template.defaulttags import URLNode


register = template.Library()


class URLCrossReferenceNode(URLNode):
    def __init__(self, filename, link_text, asvar):
        self.filename = filename
        self.link_text = link_text
        super(URLCrossReferenceNode, self).__init__('online_docs_view', [],
            {}, asvar)

    def render(self, context):
        """
        Renders the cross-link with ``class=onlineDocsCrossReference``.

        If you have JavaScript enabnled and ``online_docs.js`` loaded in your
        page, the link will trigger an AJAX request and open the docs in the
        same jQuery modal.

        """
        url = super(URLCrossReferenceNode, self).render(context)
        if self.asvar:
            url = context[self.asvar]
        url = ('<a class="onlineDocsLink" href="{0}?file={1}">'
               '{2}</a>').format(
                    url, self.filename.var, self.link_text.var)
        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


@register.simple_tag
def render_docs_link(request):
    """
    Displays a link that will open the docs for the current view.

    If you have JavaScript enabled and ``online_docs.js`` loaded in your page,
    the link will trigger an AJAX request and open the docs in a jQuery modal.

    """
    t = template.loader.get_template('online_docs/online_docs_link.html')
    ctx = template.RequestContext(request)
    return t.render(ctx)


@register.tag
def url_cross_reference(parser, token):
    """
    Creates a link to another document in your documentation.

    It expects two parameters, the ``.md`` filename of the document you want
    to load and the link text to be displayed.

    Example usage::

        {% url_cross_reference "foo_bar.md" "click here" %}
        {% url_cross_reference "foo_bar.md" "click here" as my_link %}

    """
    bits = token.split_contents()
    if len(bits) < 3 or (len(bits) < 5 and bits[-2] == 'as'):
        raise TemplateSyntaxError(
            "'%s' takes at least two arguments (name of a .md template and "
            " link text)" % bits[0])
    filename = parser.compile_filter(bits[1])
    link_text = parser.compile_filter(bits[2])
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
    return URLCrossReferenceNode(filename, link_text, asvar)
