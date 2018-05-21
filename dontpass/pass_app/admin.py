from django.contrib import admin

# Register your models here.
from .models import Quarter, Class, CapSnap, Section

admin.site.register(Class)
admin.site.register(CapSnap)
admin.site.register(Section)
admin.site.register(Quarter)
