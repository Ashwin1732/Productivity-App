from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.models import TaskGroup, TaskItem


@login_required
def dashboard(request):
    groups = (
        TaskGroup.objects.filter(user=request.user)
        .prefetch_related("tasks")
        .order_by("-created_at")
    )
    return render(request, "tasks/dashboard.html", {"groups": groups})


@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        group = TaskGroup.objects.create(user=request.user, title=title)

        descriptions = request.POST.getlist("description[]")
        dates = request.POST.getlist("date[]")

        # Enforce a maximum of 3 tasks per group at the backend as well.
        for description, due_date in list(zip(descriptions, dates))[:3]:
            if description and due_date:
                TaskItem.objects.create(
                    group=group, description=description, due_date=due_date
                )

        return redirect("dashboard")

    return render(request, "tasks/add_task.html")


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(TaskItem, id=task_id, group__user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("dashboard")


