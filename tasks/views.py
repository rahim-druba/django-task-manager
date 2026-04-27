from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskFilterForm, TaskForm
from .models import Category, Task


def home(request):
    context = {
        "total_tasks": Task.objects.count(),
        "completed_tasks": Task.objects.filter(is_completed=True).count(),
    }
    return render(request, "tasks/home.html", context)


def task_list(request):
    tasks = Task.objects.select_related("category", "priority").all()
    filter_form = TaskFilterForm(request.GET or None) #Create a filter form and fill it with URL search data if available.

    if filter_form.is_valid():
        query = filter_form.cleaned_data.get("query")
        category = filter_form.cleaned_data.get("category")
        status = filter_form.cleaned_data.get("status")

        if query:
            tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            tasks = tasks.filter(category=category)
        if status == "pending":
            tasks = tasks.filter(is_completed=False)
        elif status == "completed":
            tasks = tasks.filter(is_completed=True)

    return render(
        request,
        "tasks/task_list.html",
        {"tasks": tasks, "filter_form": filter_form},
    )


def task_detail(request, task_id):
    task = get_object_or_404(Task.objects.select_related("category", "priority"), pk=task_id)
    return render(request, "tasks/task_detail.html", {"task": task})


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully.")
            return redirect("task_list")
        messages.error(request, "Please correct the form errors.")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Create Task"})


def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect("task_detail", task_id=task.id)
        messages.error(request, "Please correct the form errors.")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Update Task"})


def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


def category_list(request):
    categories = Category.objects.prefetch_related("tasks")
    return render(request, "tasks/category_list.html", {"categories": categories})
