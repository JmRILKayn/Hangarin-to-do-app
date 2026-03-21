from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def home(request):
    return render(request, 'hangarin/home.html')

def dashboard(request):
    category_name = request.GET.get('category') # Get category from URL
    
    # Filter tasks if a category is selected
    if category_name:
        tasks = Task.objects.filter(category__name=category_name).order_by('deadline')
    else:
        tasks = Task.objects.all().order_by('deadline')
        
    from .models import Category
    categories = Category.objects.all() 
    
    return render(request, 'hangarin/dashboard.html', {
        'tasks': tasks, 
        'categories': categories,
        'selected_category': category_name  
    })

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == 'Completed':
        task.status = 'Pending'
    else:
        task.status = 'Completed'
    task.save()
    return redirect('dashboard')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('dashboard')