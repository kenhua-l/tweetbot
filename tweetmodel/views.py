from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Note, History
from TweetBotWeb import tweetbot
# Create your views here.
class NoteView(ListView):
    model = Note
    template_name = 'tweetmodel/note_list.html'
    def get_context_data(self, **kwargs):
        context = super(NoteView, self).get_context_data(**kwargs)
        context['nbar'] = 'notes'
        return context

class NoteNewView(SuccessMessageMixin, CreateView):
    model = Note
    template_name = 'tweetmodel/note_form.html'
    fields = '__all__'
    success_url = '/'
    success_message = 'New note successfully saved!!!!'
    def get_context_data(self, **kwargs):
        context = super(NoteNewView, self).get_context_data(**kwargs)
        context['nbar'] = 'notes'
        return context

class NoteEditView(UpdateView):
    model = Note
    template_name = 'tweetmodel/note_edit.html'
    fields = '__all__'
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super(NoteEditView, self).get_context_data(**kwargs)
        context['nbar'] = 'notes'
        return context

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'tweetmodel/note_confirm_delete.html'
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super(NoteDeleteView, self).get_context_data(**kwargs)
        context['nbar'] = 'notes'
        return context

class HistoryView(ListView):
    model = History
    template_name = 'tweetmodel/history_list.html'
    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['nbar'] = 'history'
        return context

def tweet_note(request, pk):
    messages.success(request, tweetbot.tweet_note(pk))
    return redirect('/')
