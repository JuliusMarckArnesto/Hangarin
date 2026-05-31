from django.shortcuts import render
from django.views.generic.list import ListView
from hangarinapp.models import Task, Note, SubTask, Category, Priority
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from hangarinapp.forms import TaskForm, NoteForm
from django.urls import reverse_lazy

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasklist'
    template_name = 'task_list.html'
    paginate_by = None

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task-list')

#---- NOTES ----
class NoteListView(ListView):
    model = Note
    context_object_name = "notelist"
    template_name = "note_list.html"
    paginate_by = None

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_delete.html'
    success_url = reverse_lazy('note-list')