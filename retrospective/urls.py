# -*- encoding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),

    url(r'^planning/create/$',
        views.PlanningCreateView.as_view(),
        name='planning-create'),
    url(r'^planning/(?P<id_plan>[-_\w]+)/$',
        views.PlanningDetailView.as_view(), name="planning"),
    url(r'^planning/edit/(?P<id_plan>[-_\w]+)/$',
        views.PlanningEditView.as_view(),
        name='planning-edit'),

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
    url(r'^profile/(?P<u_name>[-_\w]+)/$', views.ProfileView.as_view(),
        name="profile"),
    url(r'^update_user/$', views.UpdateDataUserView.as_view(),
        name="update_user"),
    url(r'^update_password/$', views.update_password, name="update_password"),
]
