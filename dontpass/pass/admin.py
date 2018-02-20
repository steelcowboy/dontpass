from django.contrib import admin

# Register your models here.
from .models import CapSnap, Section

admin.site.register(CapSnap)
admin.site.register(Section)
