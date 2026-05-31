from django.forms import ModelForm, DateTimeInput, Textarea, TextInput, Select
from django import forms
from django.utils import timezone
from .models import Task, Note, Category, Priority

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow saving even when some fields are omitted in the form
        optional_fields = ['description', 'deadline', 'category', 'priority']
        for name in optional_fields:
            if name in self.fields:
                self.fields[name].required = False

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter task description'
            }),
            'deadline': DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': Select(attrs={
                'class': 'form-control'
            }),
            'category': Select(attrs={
                'class': 'form-control'
            }),
            'priority': Select(attrs={
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Provide sensible defaults for missing fields so model save succeeds
        if not self.cleaned_data.get('deadline'):
            instance.deadline = timezone.now()
        if not self.cleaned_data.get('category'):
            cat, _ = Category.objects.get_or_create(category_name='Uncategorized')
            instance.category = cat
        if not self.cleaned_data.get('priority'):
            pr, _ = Priority.objects.get_or_create(priority_level='Normal')
            instance.priority = pr
        if not self.cleaned_data.get('description'):
            instance.description = ''
        if commit:
            instance.save()
        return instance