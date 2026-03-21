from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def home(request):
    return render(request, 'hangarin/home.html')

def dashboard(request):
    tasks = Task.objects.all().order_by('deadline')
    return render(request, 'hangarin/dashboard.html', {'tasks': tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = 'Completed'
    task.save()
    return redirect('dashboard')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('dashboard')