"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from hangarinapp.views import TaskListView, TaskCreateView
from hangarinapp import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('pwa.urls')),
    #---TASKS---
    path('', views.TaskListView.as_view(), name='task-list'), 
    path('tasks/', views.TaskListView.as_view(), name='task-list'), 
    path('tasks/add', views.TaskCreateView.as_view(), name='task-add'),
    path('tasks/<int:pk>', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),
    #---NOTES---
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/add', views.NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>', views.NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete', views.NoteDeleteView.as_view(), name='note-delete'),
    #---SUBTASKS---
    path('subtasks/add', views.SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtask/<int:pk>', views.SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtask/<int:pk>/delete', views.SubTaskDeleteView.as_view(), name='subtask-delete'),
    #---MODALS---
    path('subtask/<int:pk>/toggle', views.SubTaskToggleView.as_view(), name='subtask-toggle'),    
]
