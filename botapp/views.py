import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . models import TwitterProfile, Topic, Schedule
from django.contrib import messages
from TweetBotWeb import tweetbot

# Create your views here.
class HomePageView(ListView):
    model = TwitterProfile
    template_name = 'botapp/config_landing.html'
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['schedule'] = Schedule.objects.all()
        context['nbar'] = 'config'
        context['activeTwitterProfile'] = self.get_twitter_handle()
        return context
    def get_twitter_handle(self):
        try:
            app_token = self.model.objects.all()[0].consumer_token
            app_secret = self.model.objects.all()[0].consumer_secret
            access_token = self.model.objects.all()[0].access_token
            access_secret = self.model.objects.all()[0].access_secret
            return tweetbot.get_twitter_handle(app_token, app_secret, access_token, access_secret)
        except:
            return None

class ConfigScheduleView(UpdateView):
    model = Schedule
    fields = '__all__'
    template_name = 'botapp/config_sched.html'
    success_url = '/configuration'
    def get_context_data(self, **kwargs):
        context = super(ConfigScheduleView, self).get_context_data(**kwargs)
        context['nbar'] = 'config'
        return context

class TopicNewView(CreateView):
    model = Topic
    template_name = 'botapp/topic_form.html'
    fields = '__all__'
    success_url = '/configuration'
    def get_context_data(self, **kwargs):
        context = super(TopicNewView, self).get_context_data(**kwargs)
        context['nbar'] = 'config'
        return context

class TopicEditView(UpdateView):
    model = Topic
    template_name = 'botapp/topic_edit.html'
    fields = '__all__'
    success_url = '/configuration'
    def get_context_data(self, **kwargs):
        context = super(TopicEditView, self).get_context_data(**kwargs)
        context['nbar'] = 'config'
        return context

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'botapp/topic_confirm_delete.html'
    success_url = '/configuration'
    def get_context_data(self, **kwargs):
        context = super(TopicDeleteView, self).get_context_data(**kwargs)
        context['nbar'] = 'config'
        return context

def logView(request):
    log_to_display = getLogs()
    html = 'log.html'
    return render(request, html, {'file_' : log_to_display, 'nbar':'log'})

def download_log(request):
    file_path = os.path.join(settings.PROJECT_ROOT, 'tweetbot.log')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def delete_log_confirm(request):
    html = 'log_delete_confirm.html'
    return render(request, html, {'nbar':'log'})

def delete_log(request):
    with open(os.path.join(settings.PROJECT_ROOT, 'tweetbot.log'), 'w') as file_:
        file_.write('')
    messages.success(request, "Log is successfully deleted.")
    return redirect('/log')

def run_bot_script(request):
    messages.success(request, tweetbot.run())
    return redirect('/')

def getLogs():
    file_string = []
    with open(os.path.join(settings.PROJECT_ROOT, 'tweetbot.log')) as file_:
        for line in file_:
            file_string.append(line)
    log_to_display = '\n'.join(file_string)
    return log_to_display
