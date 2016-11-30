# -*- encoding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^retrospective/(?P<id_retro>[-_\w]+)/$',
        views.RetrospectiveDetailView.as_view(), name="retrospective"),
    url(r'^retrospective/create/(?P<id_retro>[-_\w]+)/$',
        views.RetrospectiveUserCreateView.as_view(),
        name='retrospective-create'),
    url(r'^retrospective/edit/(?P<id_retro>[-_\w]+)/$',
        views.RetrospectiveUserEditView.as_view(),
        name='retrospective-edit'),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
]
