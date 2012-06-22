"""URLs for the ``online_docs`` app."""
from django.conf.urls.defaults import patterns, url

from online_docs.views import OnlineDocsView


urlpatterns = patterns('',
    url(r'^$',
        OnlineDocsView.as_view(),
        name='online_docs_view',
    )
)
