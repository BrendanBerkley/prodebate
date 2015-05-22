from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'prodebate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^positions/', include('pro_debate.urls')),
    url(r'^$', 'pro_debate.views.index'),
    url(r'^admin/', include(admin.site.urls)),
]
