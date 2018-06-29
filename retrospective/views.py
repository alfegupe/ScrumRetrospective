# -*- encoding: utf-8 -*-
import json
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
from .forms import LoginForm, UpdateDataUserForm, UpdatePasswordUserForm, \
    SprintForm
from .models import Planning, Retrospective, RetrospectiveUser, Sprint, \
    TaskSprintUser
from django.contrib.auth.models import User


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


class IndexView(LoginRequiredMixin, View):
    template = "general/index.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        sprints = Sprint.objects.all().order_by('-id')
        plannings = Planning.objects.all().order_by('-id')
        retrospectives = Retrospective.objects.all().order_by('-id')

        context = {
            'sprints': sprints,
            'plannings': plannings,
            'retrospectives': retrospectives
        }
        return render(request, self.template, context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'u_name'
    login_url = 'login'


class UpdateDataUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/edit.html'
    login_url = 'login'
    form_class = UpdateDataUserForm

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'u_name': self.request.user.username}
        )

    def get_object(self, queryset=None):
        return self.request.user

    def get_username(self):
        return self.request.user.username


def update_password(request):
    message = None
    form = UpdatePasswordUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_pass = form.cleaned_data['password']
            new_pass = form.cleaned_data['new_password']
            if authenticate(
                    username=request.user.username, password=current_pass
            ):
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user)
                message = 'Password actualizado.'
            else:
                message = 'El password actual es incorrecto'

    context = {'form': form, 'message': message}
    return render(request, 'user/update_password.html', context)


class RetrospectiveDetailView(LoginRequiredMixin, DetailView):
    model = Retrospective
    template_name = "retrospective_user/retrospective_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id_retro"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super(RetrospectiveDetailView, self).get_context_data(**kwargs)
        data = RetrospectiveUser.objects.filter(
            retrospective=self.object
        )
        data_off = User.objects.filter(is_active=True).exclude(
            id__in=data.values_list('user', flat=True)
        )
        context['data'] = data
        context['data_off'] = data_off
        return context


class RetrospectiveUserCreateView(LoginRequiredMixin, CreateView):
    model = RetrospectiveUser
    fields = ['good', 'bad', 'suggestions']
    slug_field = 'id'
    slug_url_kwarg = 'id_retro'
    login_url = 'login'
    template_name = 'retrospective_user/retrospective_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.retrospective = Retrospective.objects.get(
                id=self.kwargs['id_retro'])
            messages.success(
                self.request, 'Retrospectiva guardada correctamente.'
            )
            return super(RetrospectiveUserCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(RetrospectiveUserCreateView, self).form_invalid(form)

    def get_success_url(self):
        if 'retro' in self.request.GET:
            retro = self.request.GET['retro']
            return reverse_lazy('retrospective', kwargs={'id_retro': retro})


class RetrospectiveUserEditView(LoginRequiredMixin, UpdateView):
    model = RetrospectiveUser
    fields = ['good', 'bad', 'suggestions']
    slug_field = 'id'
    slug_url_kwarg = 'id_retro'
    login_url = 'login'
    template_name = 'retrospective_user/retrospective_edit.html'

    def form_valid(self, form):
        try:
            messages.success(
                self.request, 'Retrospectiva actualizada correctamente.'
            )
            return super(RetrospectiveUserEditView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(RetrospectiveUserEditView, self).form_invalid(form)

    def get_success_url(self):
        if 'retro' in self.request.GET:
            retro = self.request.GET['retro']
            return reverse_lazy('retrospective', kwargs={'id_retro': retro})


class PlanningDetailView(LoginRequiredMixin, DetailView):
    model = Planning
    template_name = "planning/planning_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id_plan"
    login_url = "login"


class PlanningCreateView(LoginRequiredMixin, CreateView):
    model = Planning
    fields = ['name', 'content']
    template_name = 'planning/planning_create.html'
    success_url = reverse_lazy('index')
    login_url = 'login'

    def form_valid(self, form):
        try:
            return super(PlanningCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(PlanningCreateView, self).form_invalid(form)

    def get_success_url(self):
        plan = self.object.id
        if self.request.GET['continue'] == 'True':
            resolver = reverse_lazy('planning-edit', kwargs={'id_plan': plan})
        else:
            resolver = reverse_lazy('index')
            messages.success(
                self.request, 'Planificación fueactualizada correctamente.'
            )
        return resolver


class PlanningEditView(LoginRequiredMixin, UpdateView):
    model = Planning
    fields = ['name', 'content']
    slug_field = 'id'
    slug_url_kwarg = 'id_plan'
    login_url = 'login'
    template_name = 'planning/planning_edit.html'

    def form_valid(self, form):
        try:

            return super(PlanningEditView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(PlanningEditView, self).form_invalid(form)

    def get_success_url(self):
        plan = self.object.id
        if self.request.GET['continue'] == 'True':
            resolver = reverse_lazy('planning-edit', kwargs={'id_plan': plan})
        else:
            resolver = reverse_lazy('index')
            messages.success(
                self.request, 'Planificación fue actualizada correctamente.'
            )
        return resolver


class RetrospectiveCreateView(LoginRequiredMixin, CreateView):
    model = Retrospective
    fields = ['name']
    template_name = 'retrospective/retrospective_create.html'
    success_url = reverse_lazy('index')
    login_url = 'login'

    def form_valid(self, form):
        try:
            messages.success(
                self.request, 'Retrospectiva guardada correctamente.'
            )
            return super(RetrospectiveCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(RetrospectiveCreateView, self).form_invalid(form)

    def get_success_url(self):
        retro = self.object.id
        return reverse_lazy('retrospective', kwargs={'id_retro': retro})


class RetrospectiveEditView(LoginRequiredMixin, UpdateView):
    model = Retrospective
    fields = ['name']
    slug_field = 'id'
    slug_url_kwarg = 'id_retro'
    login_url = 'login'
    template_name = 'retrospective/retrospective_edit.html'

    def form_valid(self, form):
        try:
            messages.success(
                self.request, 'Retrospectiva actualizada correctamente.'
            )
            return super(RetrospectiveEditView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(RetrospectiveEditView, self).form_invalid(form)

    def get_success_url(self):
        retro = self.object.id
        return reverse_lazy('retrospective', kwargs={'id_retro': retro})


class SprintDetailView(LoginRequiredMixin, DetailView):
    model = Sprint
    template_name = "sprint/sprint_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id_sprint"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super(SprintDetailView, self).get_context_data(**kwargs)
        data = TaskSprintUser.objects.filter(
            sprint=self.object
        )
        data_off = User.objects.filter(is_active=True).exclude(
            id__in=data.values_list('user', flat=True)
        )
        global_tasks = ''
        if data:
            for usr in data:
                global_tasks += usr.tasks
            context['global_tasks'] = global_tasks
        context['data'] = data
        context['data_off'] = data_off
        return context


class SprintCreateView(LoginRequiredMixin, CreateView):
    model = Sprint
    form_class = SprintForm
    template_name = 'sprint/sprint_create.html'
    success_url = reverse_lazy('index')
    login_url = 'login'

    def form_valid(self, form):
        try:
            messages.success(
                self.request, 'Sprint creado correctamente.'
            )
            return super(SprintCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(SprintCreateView, self).form_invalid(form)

    def get_success_url(self):
        sprint = self.object.id
        return reverse_lazy('sprint', kwargs={'id_sprint': sprint})


class SprintEditView(LoginRequiredMixin, UpdateView):
    model = Sprint
    form_class = SprintForm
    slug_field = 'id'
    slug_url_kwarg = 'id_sprint'
    login_url = 'login'
    template_name = 'sprint/sprint_edit.html'

    def form_valid(self, form):
        try:
            messages.success(
                self.request, 'Sprint actualizado correctamente.'
            )
            return super(SprintEditView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(SprintEditView, self).form_invalid(form)

    def get_success_url(self):
        sprint = self.object.id
        return reverse_lazy('sprint', kwargs={'id_sprint': sprint})


class SprintTasksUserCreateView(LoginRequiredMixin, CreateView):
    model = TaskSprintUser
    fields = ['tasks', ]
    slug_field = 'id'
    slug_url_kwarg = 'id_sprint'
    login_url = 'login'
    template_name = 'sprint_tasks/sprint_tasks_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.sprint = Sprint.objects.get(
                id=self.kwargs['id_sprint'])
            messages.success(
                self.request, 'Tareas guardadas correctamente.'
            )
            return super(SprintTasksUserCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(SprintTasksUserCreateView, self).form_invalid(form)

    def get_success_url(self):
        if 'sprint' in self.request.GET:
            sprint = self.request.GET['sprint']
            return reverse_lazy('sprint', kwargs={'id_sprint': sprint})


class SprintTasksUserEditView(LoginRequiredMixin, UpdateView):
    model = TaskSprintUser
    fields = ['tasks', ]
    slug_field = 'id'
    slug_url_kwarg = 'id_sprint'
    login_url = 'login'
    template_name = 'sprint_tasks/sprint_tasks_edit.html'

    def form_valid(self, form):
        try:
            messages.success(
                self.request, 'Tareas actualizadas correctamente.'
            )
            return super(SprintTasksUserEditView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(SprintTasksUserEditView, self).form_invalid(form)

    def get_success_url(self):
        if 'sprint' in self.request.GET:
            sprint = self.request.GET['sprint']
            return reverse_lazy('sprint', kwargs={'id_sprint': sprint})
