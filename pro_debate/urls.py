from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<position_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit/position/(?P<position_id>[0-9]+)/$', views.edit_position, name='edit_position'),
    url(r'^add/elaboration/(?P<position_id>[0-9]+)/$', views.add_elaboration, name='add_elaboration'),
    url(r'^edit/elaboration/(?P<elaboration_id>[0-9]+)/$', views.edit_elaboration, name='edit_elaboration'),
    url(r'^tagged/(?P<tag_id>[0-9]+)/$', views.tag_index, name='tag_index'),
    url(r'^comments/', include('django_comments.urls')),
]