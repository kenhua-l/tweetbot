"""TweetBotWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tweetmodel.views import HistoryView
from botapp import views as botappViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('configuration/', include('botapp.urls')),
    path('', include('tweetmodel.urls')),
    path('history', HistoryView.as_view(), name='history'),
    path('log', botappViews.logView, name='log'),
    path('run', botappViews.run_bot_script, name='run'),
    path('download_log', botappViews.download_log, name='download_log'),
    path('delete_log_confirm', botappViews.delete_log_confirm, name='delete_log_confirm'),
    path('delete_log', botappViews.delete_log, name='delete_log'),
]
