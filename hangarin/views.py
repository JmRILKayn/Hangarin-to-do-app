from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category, Priority, Note, SubTask
from django.utils import timezone 

def dashboard(request, filter_type=None):
    # Base Querysets
    tasks = Task.objects.all().order_by('deadline')
    notes = Note.objects.all()
    subtasks = SubTask.objects.all()
    
    # Sidebar Filtering Logic
    if filter_type == 'important':
        # Filter by high-level priority
        tasks = tasks.filter(priority__name__icontains="High")
    elif filter_type == 'planned':
        tasks = tasks.exclude(deadline__isnull=True)
    elif filter_type == 'notes':
        # This will tell the HTML to show the Notes table
        pass 
    elif filter_type == 'subtasks':
        # This will tell the HTML to show the SubTasks table
        pass

    categories = Category.objects.all()
    
    # Stats for the top cards
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
        'categories': categories,
        'filter_type': filter_type,
        'stats': stats
    })

# --- Task Actions ---
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        default_cat, _ = Category.objects.get_or_create(name="General")
        default_prio, _ = Priority.objects.get_or_create(name="Medium")
        
        if title:
            Task.objects.create(
                title=title,
                description="", # Added to prevent null error
                category=default_cat,
                priority=default_prio,
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