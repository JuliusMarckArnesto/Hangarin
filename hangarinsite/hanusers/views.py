from django.shortcuts import render
from .models import Task, Note

def dashboard_view(request):
    # Fetching 3 notes for the dashboard cards
    recent_notes = Note.objects.all()[:3]
    # Fetching all tasks
    tasks = Task.objects.select_related('priority', 'category').all()
    
    return render(request, 'dashboard.html', {
        'notes': recent_notes,
        'tasks': tasks
    })