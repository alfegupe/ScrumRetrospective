# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, \
    update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, \
    RedirectView, View
from django.views.generic.edit import UpdateView


class IndexView(View):
    template = "retrospective/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})
