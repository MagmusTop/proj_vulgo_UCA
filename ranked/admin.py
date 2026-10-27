from django.contrib import admin

# Register your models here.
from .models.models import *

admin.site.register(Rank)
admin.site.register(Visitor)