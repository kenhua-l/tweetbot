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

from django.urls import path, include
from tweetmodel import views

urlpatterns = [
    path('', views.NoteView.as_view(), name='notes'),
    path('new/', views.NoteNewView.as_view(), name='note_new'),
    path('<int:pk>/edit/', views.NoteEditView.as_view(), name='note_edit'),
    path('<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('<int:pk>/tweet_note/', views.tweet_note, name='tweet_note')
]
