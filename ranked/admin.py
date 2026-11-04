from django.contrib import admin

# Register your models here.
from .models.models import *

admin.site.register(Comment)
admin.site.register(Visitor)
admin.site.register(Vote)