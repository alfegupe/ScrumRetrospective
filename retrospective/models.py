# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from django import forms


class Sprint(models.Model):
    name = models.CharField(max_length=250)
    date_start = models.DateField()
    date_finish = models.DateField()
    planning = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Planning(models.Model):
    name = models.CharField(max_length=250)
    content = HTMLField()
    user = models.ForeignKey(User, null=True, blank=True, default=15)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Planificación'
        verbose_name_plural = 'Planificaciones'


class Retrospective(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Retrospectiva'


class RetrospectiveUser(models.Model):
    retrospective = models.ForeignKey(Retrospective, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    good = HTMLField()
    bad = HTMLField()
    suggestions = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('retrospective', 'user'),)
        verbose_name_plural = 'Retrospectivas por usuario'

    def __unicode__(self):
        return self.retrospective.name + ': ' + self.user.username


class TaskSprintUser(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('sprint', 'user'),)
        verbose_name = 'Tareas usuario por Sprint'
        verbose_name_plural = 'Tareas usuarios por Sprint'

    def __unicode__(self):
        return self.sprint.name + ': ' + self.user.username
