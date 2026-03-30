"""
URL configuration for hangarinsite project.

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
from django.urls import path 
from hanusers.views import DashboardView, TaskList, TaskCreateView, TaskUpdateView, TaskDeleteView, NoteList, NoteCreateView, NoteUpdateView, NoteDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    #____TASKS____
    path('task_list', TaskList.as_view(), name='task-list'),
    path('task_list/add', TaskCreateView.as_view(), name='task-add'),
    path('task_list/<pk>', TaskUpdateView.as_view(), name='task-update'),
    path('task_list/<pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    #____NOTES____
    path('note_list', NoteList.as_view(), name='note-list'),
    path('note_list/add', NoteCreateView.as_view(), name='note-add'),
    path('note_list/<pk>', NoteUpdateView.as_view(), name='note-update'),
    path('note_list/<pk>/delete', NoteDeleteView.as_view(), name='note-delete'),
]
