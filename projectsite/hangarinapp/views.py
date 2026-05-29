from django.shortcuts import render
from django.views.generic.list import ListView
from hangarinapp.models import Task

class TaskListView(ListView):
    model = Task
    context_object_name = 'taskpage'
    template_name = 'main_page.html'