"""Views for the ``online_docs`` app."""
import os

from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import Http404
from django.template import Template, RequestContext
from django.views.generic import TemplateView


class OnlineDocsView(TemplateView):
    """View that displays the docs for the current URL path."""
    def dispatch(self, request, *args, **kwargs):
        self.path = request.GET.get('path')
        if not self.path:
            raise Http404
        return super(OnlineDocsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(OnlineDocsView, self).get_context_data(**kwargs)
        document_name = self.get_document_name()
        file_path = self.get_document_file_path(document_name)
        document_content = self.get_document_content(file_path)
        ctx.update({
            'docs': document_content,
            'document_name': document_name,
            'DEBUG': settings.DEBUG,
        })
        return ctx

    def get_document_name(self):
        url = resolve(self.path)
        document_name = '%s.md' % url.view_name.replace(':', '_')
        return document_name

    def get_document_file_path(self, document_name):
        file_path = os.path.join(settings.STATIC_ROOT, 'online_docs',
            document_name)
        return file_path

    def get_document_content(self, file_path):
        try:
            f = open(file_path, 'r')
            document = f.read()
        except IOError:
            return None
        ctx = RequestContext(self.request)
        return Template(document).render(ctx)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['online_docs/partials/online_docs.html', ]
        else:
            return ['online_docs/online_docs.html', ]
