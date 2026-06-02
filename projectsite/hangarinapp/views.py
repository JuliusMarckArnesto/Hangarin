from django.shortcuts import render
from django.views.generic.list import ListView
from hangarinapp.models import Task, Note, SubTask, Category, Priority
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from hangarinapp.forms import TaskForm, NoteForm, SubTaskForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasklist'
    template_name = 'task_list.html'
    paginate_by = None

    def get_queryset(self):
        qs = super().get_queryset()

        #---SEARCH---
        query = self.request.GET.get('q')
        if query:
            qs =qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        #---SORTING---
        sort_options = {
            'deadline':  'deadline',
            '-deadline': '-deadline',
            'title':     'title',
            '-title':    '-title',
            'status':    'status',
            'priority':  'priority__priority_level',
            'category':  'category__category_name',
            'created':   'created_at',
            '-created':  '-created_at',
        }
        sort_by = self.request.GET.get('sort_by', 'deadline') # sort from templates
        order = sort_options.get(sort_by, 'deadline')# sort from here
        qs = qs.order_by(order)

        return qs
    
        #---CONTEXT---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()

        today = timezone.now().date()

        count = (
            Task.objects.filter(created_at__year=today.year).count(),
            Task.objects.filter(created_at__month=today.month).count(),
        )
        context['tasks_this_year'] = count[0]
        context['task_this_month'] = count[1]

        context['task_pending'] = Task.objects.filter(status="Pending").count()
        context['task_inprogress'] = Task.objects.filter(status="In Progress").count()
        context['task_completed'] = Task.objects.filter(status="Completed").count()

        context['priority_high'] = Task.objects.filter(priority__priority_level="high").count()
        context['priority_medium'] = Task.objects.filter(priority__priority_level="medium").count()
        context['priority_low'] = Task.objects.filter(priority__priority_level="low").count()
        context['priority_optional'] = Task.objects.filter(priority__priority_level="optional").count()

        context['category_work'] = Task.objects.filter(category__category_name="Work").count()
        context['category_school'] = Task.objects.filter(category__category_name="School").count()
        context['category_personal'] = Task.objects.filter(category__category_name="Personal").count()
        context['category_optional'] = Task.objects.filter(category__category_name="Optional").count()

        context['overdue_tasks'] = Task.objects.filter(deadline__lt=today).exclude(status='Completed').count()
        context['due_soon'] = Task.objects.filter(deadline__range=(today, today + timezone.timedelta(hours=24))).exclude(status='Completed').count()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task-list')

#---- NOTES ----
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = "notelist"
    template_name = "note_list.html"
    paginate_by = None

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(task__title__icontains=query) |
                Q(content__icontains=query)
            )

        #---SORTING---
        sort_options = {
            'content':  'content',
            '-content': '-content',
            'title':     'task__title',
            '-title':    '-task__title',
            'created':   'created_at',
            '-created':  '-created_at',
            'updated':   'updated_at',
            '-updated':  '-updated_at',
        }
        sort_by = self.request.GET.get('sort_by', '-created')
        order = sort_options.get(sort_by, '-created')
        qs = qs.order_by(order)

        return qs
    #---CONTEXT---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_notes'] = Note.objects.count()

        today = timezone.now().date()
        count = (
            Note.objects.filter(created_at__year=today.year).count(),
            Note.objects.filter(created_at__month=today.month).count(),
        )
        context['notes_this_year'] = count[0]
        context['notes_this_month'] = count[1]
        return context

class NoteNoteTaskModal(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = "notetasklist"
    template_name = "task_list.html"
    paginate_by = None

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    
    def get_success_url(self):
        source = self.request.POST.get('source', 'note-list')
        return reverse_lazy(source)

class NoteUpdateView(LoginRequiredMixin,UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    
    def get_success_url(self):
        source = self.request.POST.get('source', 'note-list')
        return reverse_lazy(source)

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_delete.html'
    
    def get_success_url(self):
        source = self.request.POST.get('source', 'note-list')
        return reverse_lazy(source)

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get('task') 
        if task_id:
            initial['parent_task'] = task_id
        return initial

    def get_success_url(self):
        source = self.request.POST.get('source', 'task-list')
        return reverse_lazy(source)

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"

    def get_success_url(self):
        source = self.request.POST.get('source', 'task-list')
        return reverse_lazy(source)

class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'subtask_delete.html'

    def get_success_url(self):
        source = self.request.POST.get('source', 'task-list')
        return reverse_lazy(source)

class SubTaskToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        if subtask.subtask_status == "Completed":
            subtask.subtask_status = "Pending"
        else:
            subtask.subtask_status = "Completed"
        subtask.save()
        return redirect(request.POST.get('source', 'task-list'))