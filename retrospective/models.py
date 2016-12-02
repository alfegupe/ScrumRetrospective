# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE


class Planning(models.Model):
    name = models.CharField(max_length=250)
    content = HTMLField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Planificación'
        verbose_name_plural = 'Planificaciones'


class Retrospective(models.Model):
    name = models.CharField(max_length=250)

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

    class Meta:
        unique_together = (('retrospective', 'user'),)
        verbose_name_plural = 'Retrospectivas por usuario'

    def __unicode__(self):
        return self.retrospective.name + ': ' + self.user.username
