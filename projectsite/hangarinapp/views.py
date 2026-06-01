from django.shortcuts import render
from django.views.generic.list import ListView
from hangarinapp.models import Task, Note, SubTask, Category, Priority
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from hangarinapp.forms import TaskForm, NoteForm, SubTaskForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
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

class NoteNoteTaskModal(ListView):
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

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    
    def get_success_url(self):
        source = self.request.POST.get('source', 'note-list')
        return reverse_lazy(source)

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_delete.html'
    
    def get_success_url(self):
        source = self.request.POST.get('source', 'note-list')
        return reverse_lazy(source)

class SubTaskCreateView(CreateView):
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

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"

    def get_success_url(self):
        source = self.request.POST.get('source', 'task-list')
        return reverse_lazy(source)

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_delete.html'

    def get_success_url(self):
        source = self.request.POST.get('source', 'task-list')
        return reverse_lazy(source)

class SubTaskToggleView(View):
    def post(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        if subtask.subtask_status == "Completed":
            subtask.subtask_status = "Pending"
        else:
            subtask.subtask_status = "Completed"
        subtask.save()
        return redirect(request.POST.get('source', 'task-list'))