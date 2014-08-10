from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from my_django.settings import ON_DEV_SERV
from my_django.views import Index

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^$', Index.as_view(), name='index'),
)

if ON_DEV_SERV:
    urlpatterns += staticfiles_urlpatterns()

    # debug_toolbar settings
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
