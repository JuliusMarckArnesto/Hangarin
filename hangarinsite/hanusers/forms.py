from django.forms import ModelForm
from django import forms
from .models import Task, Note, SubTask

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
        
        widgets = {
            # Date and Time Picker
            'deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            # ForeignKeys & Choices (Standard Select)
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            # Text inputs
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = "__all__"
class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = "__all__"