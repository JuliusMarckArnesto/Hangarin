from django.shortcuts import render
from django.views.generic.list import ListView
from hangarinapp.models import Task, Note, SubTask, Category, Priority

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasklist'
    template_name = 'task_list.html'
    paginate_by = None