# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, \
    update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, \
    RedirectView, View, FormView
from django.views.generic.edit import UpdateView


class IndexView(View):
    template = "retrospective/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        else:
            return super(
                LoginRequiredMixin, self).dispatch(request, *args, **kwargs)