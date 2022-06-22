from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

admin.site.register(Share)
admin.site.register(NewsKeyWord)
admin.site.register(News)