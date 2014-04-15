from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ctfstore.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'django.contrib.auth.views.login'}),
    url(r'^$', 'store.views.home', name='home'),
    url(r'^achievements$', 'store.views.achievements', name='achievements'),
    url(r'^upgrades$', 'store.views.upgrades', name='upgrades'),
    url(r'^upgrades/order$', 'store.views.order_upgrade', name='upgrade_order'),
    url(r'^career$', 'store.views.career', name='career'),
    url(r'^contact$', 'store.views.contact', name='contact'),

    url(r'^api/redeem/(?P<user_id>\d+)/(?P<unlock_key>\w+)$', 'store.views.api_redeem', name='api_redeem'),
    url(r'^api/has/(?P<unlock_key>\w+)$$', 'store.views.api_has', name='api_redeem'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT})
    )