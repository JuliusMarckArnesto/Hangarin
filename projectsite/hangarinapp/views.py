from django.shortcuts import render
from django.views.generic.list import ListView
from hangarinapp.models import Task, Note, SubTask, Category, Priority
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from hangarinapp.forms import TaskForm
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

#---- NOTES ----
class NoteListView(ListView):
    model = Note
    context_object_name = "notelist"
    template_name = "note_list.html"
    paginate_by = None