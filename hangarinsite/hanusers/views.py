from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task, Note
from hanusers.forms import TaskForm, NoteForm
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
class TaskList(ListView):
    model = Task
    context_object_name = 'task'
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

#____TASK____
class NoteList(ListView):
    model = Note
    context_object_name = 'note'
    template_name = 'note_list.html'
    paginate_by = 5

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = "note_del.html"
    success_url = reverse_lazy('note-list')