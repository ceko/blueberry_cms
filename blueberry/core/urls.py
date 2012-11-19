from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import blueberry.core.packages

from django.conf import settings

urlpatterns = []

for ps in blueberry.core.packages.settings.get_package_settings(settings.PACKAGES):
    urlpatterns += ps.urlpatterns()

urlpatterns += patterns('core.views',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<path>.*)$', 'request_processor', name='request_processor'),
)
