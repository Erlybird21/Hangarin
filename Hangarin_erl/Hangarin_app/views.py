from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm
from django import forms


# --------------------------
# DASHBOARD VIEW
# --------------------------


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tasks = Task.objects.all()
        context["total_tasks"] = tasks.count()
        context["completed_tasks"] = tasks.filter(status="completed").count()
        context["pending_tasks"] = tasks.filter(status="pending").count()
        context["overdue_tasks"] = tasks.filter(deadline__lt=timezone.now(), status__in=["pending", "in_progress"]).count()
        context["recent_tasks"] = tasks.order_by("-created_at")[:5]  # last 5 tasks only
        
        return context


class TaskListView(ListView):
    model = Task
    template_name = 'Task_List.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_ordering(self):
        return self.request.GET.get("sort", "-created_at")

    def get_queryset(self):
        qs = super().get_queryset().select_related("priority", "category")
        query = self.request.GET.get("q")  # Get search term
        
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(priority__name__icontains=query)
            )

        return qs.order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'Task_Form.html'
    success_url = reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'Task_Form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'Task_Delete.html'
    success_url = reverse_lazy('task-list')


class CategoryListView(ListView):
    model = Category
    template_name = 'Category_List.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_ordering(self):
        return self.request.GET.get("sort", "-created_at")  # ✅


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'Category_Form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'Category_Form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'Category_Delete.html'
    success_url = reverse_lazy('category-list')

class PriorityListView(ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities'
    paginate_by = 20

    def get_ordering(self):
        return self.request.GET.get("sort", "-created_at")  # ✅

class PriorityCreateView(CreateView):
    model = Priority
    fields = ['name']
    template_name = 'Priority_Form.html'
    success_url = reverse_lazy('priority-list')


class PriorityUpdateView(UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'Priority_Form.html'
    success_url = reverse_lazy('priority-list')


class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'Priority_Delete.html'
    success_url = reverse_lazy('priority-list')


class SubTaskListView(ListView):
    model = SubTask
    template_name = "Subtask_List.html"
    context_object_name = "subtasks"
    paginate_by = 10

    def get_ordering(self):
        return self.request.GET.get("sort", "-created_at")

    def get_queryset(self):
        qs = super().get_queryset().select_related("task", "task__priority", "task__category")
        
        # --- Filters ---
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        priority = self.request.GET.get("priority")

        # Search
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(task__title__icontains=query)
            )

        # Filter by Category (if not "all")
        if category and category != "all":
            qs = qs.filter(task__category__id=category)

        # Filter by Priority (if not "all")
        if priority and priority != "all":
            qs = qs.filter(task__priority__id=priority)

        return qs.order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["priorities"] = Priority.objects.all()
        context["categories"] = Category.objects.all()
        context["search_query"] = self.request.GET.get("q", "")
        return context

class SubTaskCreateView(CreateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'SubTask_Form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskUpdateView(UpdateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'SubTask_Form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'SubTask_Delete.html'
    success_url = reverse_lazy('subtask-list')

class NoteListView(ListView):
    model = Note
    template_name = 'Notes_List.html'
    context_object_name = 'notes'
    paginate_by = 20

    def get_ordering(self):
        return self.request.GET.get("sort", "-created_at")  # ✅

class NoteCreateView(CreateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'Notes_Form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'Notes_Form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'Notes_Delete.html'
    success_url = reverse_lazy('note-list')

