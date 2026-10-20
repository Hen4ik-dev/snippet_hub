from django.contrib import admin
from . import models
# Register your models here.

mdls = [models.Profile, models.Tag, models.Snippet]

for mdl in mdls:
    admin.site.register(mdl)