from django.contrib import admin

# Register your models here.
from .models import Note, History
admin.site.register(Note)
admin.site.register(History)
