"""Views for the ``online_docs`` app."""
from django.core.urlresolvers import resolve
from django.http import Http404
from django.template import loader, RequestContext, TemplateDoesNotExist
from django.views.generic import TemplateView

from online_docs.app_settings import DOCS_DEBUG


class OnlineDocsView(TemplateView):
    """View that displays the docs for the current URL path."""
    def dispatch(self, request, *args, **kwargs):
        self.path = request.GET.get('path')
        self.file = request.GET.get('file')
        if not self.path and not self.file:
            raise Http404
        return super(OnlineDocsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(OnlineDocsView, self).get_context_data(**kwargs)
        document_name = self.get_document_name()

        try:
            template = loader.get_template('online_docs/' + document_name)
            template_ctx = RequestContext(self.request)
            template_rendered = template.render(template_ctx)
        except TemplateDoesNotExist:
            template_rendered = None

        ctx.update({
            'docs': template_rendered,
            'document_name': document_name,
            'ONLINE_DOCS_DEBUG': DOCS_DEBUG,
        })
        return ctx

    def get_document_name(self):
        if self.file:
            return self.file
        url = resolve(self.path)
        document_name = '%s.md' % url.view_name.replace(':', '_')
        return document_name

    def get_template_names(self):
        if self.request.is_ajax():
            return ['online_docs/partials/online_docs.html', ]
        else:
            return ['online_docs/online_docs.html', ]
