"""Templatetags for the ``online_docs`` app."""
from django import template


register = template.Library()


@register.simple_tag
def render_docs_link(request):
    t = template.loader.get_template('online_docs/online_docs_link.html')
    ctx = template.RequestContext(request)
    return t.render(ctx)
