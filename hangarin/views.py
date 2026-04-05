from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from django.utils import timezone 

def home(request):
    return render(request, 'hangarin/home.html')

def dashboard(request, filter_type=None):
    category_name = request.GET.get('category')
    tasks = Task.objects.all().order_by('deadline')
    
    if filter_type == 'important':
        tasks = tasks.filter(is_important=True) 
    elif filter_type == 'planned':
        tasks = tasks.exclude(deadline__isnull=True)
    
    if category_name:
        tasks = tasks.filter(category__name=category_name)
        
    categories = Category.objects.all() 
    
    return render(request, 'hangarin/dashboard.html', {
        'tasks': tasks, 
        'categories': categories,
        'selected_category': category_name,
        'filter_type': filter_type
    })

def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        
        default_category = Category.objects.first()
        
        if title and default_category:
            Task.objects.create(
                title=title,
                category=default_category, 
                status='Pending',
                deadline=timezone.now().date()
            )
        elif title and not default_category:
            new_cat = Category.objects.create(name="General")
            Task.objects.create(
                title=title,
                category=new_cat,
                status='Pending',
                deadline=timezone.now().date()
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
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('dashboard')