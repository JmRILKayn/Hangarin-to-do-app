from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category, Priority, Note, SubTask
from django.utils import timezone

def home(request):
    return render(request, 'hangarin/home.html')

def dashboard(request, filter_type=None):
    tasks = Task.objects.all().order_by('deadline')
    notes = Note.objects.all()
    subtasks = SubTask.objects.all()
    
    if filter_type == 'important':
        tasks = tasks.filter(priority__name__icontains="High")
    elif filter_type == 'planned':
        tasks = tasks.exclude(deadline__isnull=True)

    stats = {
        'total_tasks': Task.objects.count(),
        'total_notes': Note.objects.count(),
        'total_subtasks': SubTask.objects.count(),
        'completed_tasks': Task.objects.filter(status='Completed').count()
    }

    return render(request, 'hangarin/dashboard.html', {
        'tasks': tasks,
        'notes': notes,
        'subtasks': subtasks,
        'filter_type': filter_type,
        'stats': stats
    })

def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            # Safely get or create defaults to avoid IntegrityErrors
            cat, _ = Category.objects.get_or_create(name="General")
            prio, _ = Priority.objects.get_or_create(name="Medium")
            
            Task.objects.create(
                title=title,
                description="No description provided.",
                category=cat,
                priority=prio,
                status='Pending',
                deadline=timezone.now()
            )
    return redirect('dashboard')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_title = request.GET.get('title')
    if new_title:
        task.title = new_title
        task.save()
    return redirect('dashboard')

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = 'Pending' if task.status == 'Completed' else 'Completed'
    task.save()
    return redirect('dashboard')

def delete_task(request, task_id):
    get_object_or_404(Task, id=task_id).delete()
    return redirect('dashboard')