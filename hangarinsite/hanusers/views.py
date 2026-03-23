from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task, Note
from hanusers.forms import TaskForm
from django.urls import reverse_lazy

class DashboardView(ListView):
    model = Task
    context_object_name = 'task'  # This is what you loop over in the table
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Optimized fetch for recent notes
        context["notes"] = Note.objects.select_related('task').all()[:3]
        
        # to avoid hitting the database inside the loop (N+1 problem)
        context["tasks"] = Task.objects.select_related('priority', 'category').all()
        
        return context
#____TASK____
class TaskListView(ListView):
    model = Task
    context_object_name = 'task-list'
    template_name = 'task_list.html'
    paginate_by = 5

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_del.html"
    success_url = reverse_lazy('task-list')
