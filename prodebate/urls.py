from django.conf.urls import include, url
from django.contrib import admin, auth

urlpatterns = [
    # Examples:
    # url(r'^$', 'prodebate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^positions/', include('pro_debate.urls')),
    url(r'^manifestations/$', 'pro_debate.views.manifestation_index', 
        name='manifestation_index'),
    url(r'^manifestations/(?P<manifestation_id>[0-9]+)/$', 
        'pro_debate.views.manifestation', name='manifestation'),
    url(r'^$', 'pro_debate.views.index'),
    url(r'^admin/', include(admin.site.urls)),
]
