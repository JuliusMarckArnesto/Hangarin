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
        qs = Task.objects.filter(user=self.request.user)

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
        user_task = Task.objects.filter(user=self.request.user)
        context['total_tasks'] = user_task.count()

        today = timezone.now().date()

        count = (
            user_task.filter(created_at__year=today.year).count(),
            user_task.filter(created_at__month=today.month).count(),
        )
        context['tasks_this_year'] = count[0]
        context['tasks_this_month'] = count[1]

        context['task_pending'] = user_task.filter(status="Pending").count()
        context['task_inprogress'] = user_task.filter(status="In Progress").count()
        context['task_completed'] = user_task.filter(status="Completed").count()

        context['priority_high'] = user_task.filter(priority__priority_level="high").count()
        context['priority_medium'] = user_task.filter(priority__priority_level="medium").count()
        context['priority_low'] = user_task.filter(priority__priority_level="low").count()
        context['priority_optional'] = user_task.filter(priority__priority_level="optional").count()

        context['category_work'] = user_task.filter(category__category_name="Work").count()
        context['category_school'] = user_task.filter(category__category_name="School").count()
        context['category_personal'] = user_task.filter(category__category_name="Personal").count()
        context['category_optional'] = user_task.filter(category__category_name="Optional").count()

        context['overdue_tasks'] = user_task.filter(deadline__lt=today).exclude(status='Completed').count()
        context['due_soon'] = user_task.filter(deadline__range=(today, today + timezone.timedelta(hours=24))).exclude(status='Completed').count()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
        qs = Note.objects.filter(user=self.request.user)

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
        user_notes = Note.objects.filter(task__user=self.request.user)

        context['total_notes'] = user_notes.count()

        today = timezone.now().date()
        count = (
            user_notes.filter(created_at__year=today.year).count(),
            user_notes.filter(created_at__month=today.month).count(),
        )
        context['notes_this_year'] = count[0]
        context['notes_this_month'] = count[1]
        return context

class NoteCreateView(LoginRequiredMixin,CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        source = self.request.POST.get('source', 'note-list')
        return reverse_lazy(source)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
 
    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get('task')
        if task_id:
            initial['parent_task'] = task_id
        return initial

    def get_success_url(self):
        source = self.request.POST.get('source', 'task-list')
        return reverse_lazy(source)
    
    def form_valid(self, form):
        return super().form_valid(form)

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
 
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
        subtask = get_object_or_404(SubTask, pk=pk, parent_task__user=request.user)
        if subtask.subtask_status == "Completed":
            subtask.subtask_status = "Pending"
        else:
            subtask.subtask_status = "Completed"
        subtask.save()
        return redirect(request.POST.get('source', 'task-list'))