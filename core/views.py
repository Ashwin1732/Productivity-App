from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import TaskGroup, TaskItem

from django.shortcuts import get_object_or_404

@login_required
def toggle_task(request, task_id):
    # 1. Find the specific task belonging to the user
    task = get_object_or_404(TaskItem, id=task_id, group__user=request.user)
    
    # 2. Flip the switch (If True, make False. If False, make True)
    task.is_completed = not task.is_completed
    task.save()
    
    # 3. Reload the dashboard
    return redirect('dashboard')

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/index.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        if password != confirm:
            return render(request, 'core/signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=email).exists():
            return render(request, 'core/signup.html', {'error': 'Email already exists'})
        User.objects.create_user(username=email, email=email, password=password)
        return redirect('login')
    return render(request, 'core/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    groups = TaskGroup.objects.filter(user=request.user).prefetch_related('tasks')
    return render(request, 'core/dashboard.html', {'groups': groups})

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        group = TaskGroup.objects.create(user=request.user, title=title)
        descriptions = request.POST.getlist('description[]')
        dates = request.POST.getlist('date[]')
        
        for i in range(len(descriptions)):
            if descriptions[i] and dates[i]:
                TaskItem.objects.create(group=group, description=descriptions[i], due_date=dates[i])
        return redirect('dashboard')
    return render(request, 'core/add_task.html')
