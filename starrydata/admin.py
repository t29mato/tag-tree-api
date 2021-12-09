from django.contrib import admin
from .models import Tag, Node

# Register your models here.
admin.site.register([Tag, Node])
