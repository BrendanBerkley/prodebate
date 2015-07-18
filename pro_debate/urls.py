from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<position_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^tagged/(?P<tag_id>[0-9]+)/$', views.tag_index, name='tag_index'),
    url(r'^comments/', include('django_comments.urls')),
]