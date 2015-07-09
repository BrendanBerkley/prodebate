from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<position_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<position_id>[0-9]+)/submit/$', views.submit, name='submit'),
    url(r'^(?P<position_id>[0-9]+)/submit-manifestation/$', views.submit_manifestation, name='submit_manifestation'),
    # url(r'^add/$', views.add, name='add'),
    url(r'^comments/', include('django_comments.urls')),
    # url(r'^(?P<position_id>[0-9]+)/(?P<parent_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<position_id>[0-9]+)/((?P<parent_id>[0-9]+))?/$', views.detail, name='detail'),
]