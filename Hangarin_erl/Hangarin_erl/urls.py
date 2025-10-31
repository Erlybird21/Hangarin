"""
URL configuration for Hangarin_erl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from Hangarin_app import views
from Hangarin_app.views import DashboardView, TaskListView, CategoryListView, PriorityListView, SubTaskListView, NoteListView, TaskCreateView, TaskUpdateView, TaskDeleteView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,PriorityCreateView, PriorityUpdateView, PriorityDeleteView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView,NoteCreateView, NoteUpdateView, NoteDeleteView
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import FileResponse
from pathlib import Path

# """
# URL configuration for Hangarin_main project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

def service_worker(request):
    sw_path = Path(__file__).resolve().parent.parent / "static/js/serviceworker.js"
    return FileResponse(open(sw_path, "rb"), content_type="application/javascript")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("serviceworker.js", service_worker, name="serviceworker"),

    # Main app
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path('', DashboardView.as_view(), name='home'),

    # Tasks
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task-add'),
    path('tasks/<pk>/edit/', views.TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),
    path('categories/<pk>/edit/', views.CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    # Priorities
    path('priorities/', views.PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', views.PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<pk>/edit/', views.PriorityUpdateView.as_view(), name='priority-edit'),
    path('priorities/<pk>/delete/', views.PriorityDeleteView.as_view(), name='priority-delete'),

    # SubTasks
    path('subtasks/', views.SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add/', views.SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<pk>/edit/', views.SubTaskUpdateView.as_view(), name='subtask-edit'),
    path('subtasks/<pk>/delete/', views.SubTaskDeleteView.as_view(), name='subtask-delete'),

    # Notes
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/add/', views.NoteCreateView.as_view(), name='note-add'),
    path('notes/<pk>/edit/', views.NoteUpdateView.as_view(), name='note-edit'),
    path('notes/<pk>/delete/', views.NoteDeleteView.as_view(), name='note-delete'),

    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),

    # ✅ Move this to the bottom
    path('', include('pwa.urls')),
]

