from django.contrib import admin

# Register your models here.
from .models import TwitterProfile,Topic, Schedule
admin.site.register(Topic)
admin.site.register(TwitterProfile)
admin.site.register(Schedule)
