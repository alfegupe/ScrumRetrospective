# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, \
    update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, \
    RedirectView, View, FormView
from django.views.generic.edit import UpdateView
from .forms import LoginForm
from .models import Planning, Retrospective, RetrospectiveUser
from django.contrib.auth.models import User


class IndexView(View, LoginRequiredMixin):
    template = "retrospective/index.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        plannings = Planning.objects.all()
        retrospectives = Retrospective.objects.all()

        context = {
            'plannings': plannings,
            'retrospectives': retrospectives
        }
        return render(request, self.template, context)


class LoginView(View):
    form = LoginForm()
    message = None
    template = "auth/login.html"
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')

        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            self.message = 'Usuario o password incorrectos'
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message': self.message}


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RetrospectiveDetailView(DetailView, LoginRequiredMixin):
    model = Retrospective
    template = "retrospective/retrospective_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id_retro"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(RetrospectiveDetailView, self).get_context_data(**kwargs)
        data = RetrospectiveUser.objects.filter(
            retrospective=self.object
        )
        data_off = User.objects.exclude(
            id__in=RetrospectiveUser.objects.values_list('id', flat=True)
        )
        context['data'] = data
        context['data_off'] = data_off
        return context


class RetrospectiveUserCreateView(CreateView, LoginRequiredMixin):
    model = RetrospectiveUser
    fields = ['good', 'bad', 'suggestions']
    slug_field = 'id'
    slug_url_kwarg = 'id_retro'
    login_url = 'login'
    template_name = 'retrospective/retrospective_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.retrospective = Retrospective.objects.get(
                id=self.kwargs['id_retro'])
            return super(RetrospectiveUserCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(RetrospectiveUserCreateView, self).form_invalid(form)


class RetrospectiveUserEditView(UpdateView, LoginRequiredMixin):
    model = RetrospectiveUser
    fields = ['good', 'bad', 'suggestions']
    slug_field = 'id'
    slug_url_kwarg = 'id_retro'
    login_url = 'login'
    template_name = 'retrospective/retrospective_edit.html'

    def get_success_url(self):
        if self.request.GET['retro']:
            retro = self.request.GET['retro']
            return reverse_lazy('retrospective', kwargs={'id_retro': retro})
