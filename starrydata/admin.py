from django.contrib import admin
from .models import Tag, Node, TagTree

# Register your models here.
admin.site.register([Tag, Node, TagTree])
