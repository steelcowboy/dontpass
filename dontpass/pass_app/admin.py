from django.contrib import admin

# Register your models here.
from .models import Class, CapSnap, Section

admin.site.register(Class)
admin.site.register(CapSnap)
admin.site.register(Section)
