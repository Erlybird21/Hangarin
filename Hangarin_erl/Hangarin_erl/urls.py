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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    """
URL configuration for Hangarin_main project.

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
from django.urls import path
from Hangarin_app import views
from Hangarin_app.views import DashboardView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path("accounts/", include("allauth.urls")),
    path("", DashboardView.as_view(), name="dashboard"),
    # For my tasks in url
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task-add'),
    path('tasks/<pk>/edit/', views.TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    
    # For my categories in url
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

]

]
