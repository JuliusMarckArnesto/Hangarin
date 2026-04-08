from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task, Note, SubTask
from hanusers.forms import TaskForm, NoteForm, SubTaskForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models.functions import Lower

class DashboardView(ListView):
    model = Task
    context_object_name = 'task'  # This is what you loop over in the table
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Optimized fetch for recent notes
        context["notes"] = Note.objects.select_related('task').all()[:3]
        
        # to avoid hitting the database inside the loop (N+1 problem)
        context["tasks"] = Task.objects.select_related('priority', 'category').all().order_by('priority__priority_level')
        
        return context
#____TASK____
class TaskList(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 20

    def get_ordering(self):
        allowed = ["title", "-title", "created_at", "-created_at"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "title"

    def get_queryset(self):
        qs =  super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
            )
        ordering = self.get_ordering()
        if ordering == 'title':
            qs = qs.annotate(lower_title=Lower('title')).order_by('lower_title')
        elif ordering == '-title':
            qs = qs.annotate(lower_title=Lower('title')).order_by('-lower_title')
        else:
            # Django's order_by() expects the field name as a string
            qs = qs.order_by(ordering)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.all()

        context['total_tasks'] = tasks.count()
        context['completed_count'] = tasks.filter(status='completed').count()
        context['in_progress_count'] = tasks.filter(status='in_progress').count()
        context['pending_count'] = tasks.filter(status='pending').count()

        return context

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

#____NOTE____
class NoteList(ListView):
    model = Note
    context_object_name = 'note'
    template_name = 'note_list.html'
    paginate_by = None

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

#____SUBTASK____
class SubTaskList(ListView):
    model = SubTask
    context_object_name = 'subtask'
    template_name = 'subtask_list.html'
    paginate_by = None

    def get_queryset(self):
        # self.kwargs['pk'] is the ID from the URL
        context = SubTask.objects.filter(parents_task=self.kwargs['pk'])

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the parent task to the template so you can show its title
        context['parent_task'] = Task.objects.get(pk=self.kwargs['pk'])
        return context

class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "subtask_del.html"
    success_url = reverse_lazy('subtask-list')