from django.contrib import admin
from models import *

admin.site.register([
    Sprint, Planning, Retrospective, RetrospectiveUser, TaskSprintUser
])
