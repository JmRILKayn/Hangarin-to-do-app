from django.shortcuts import render
from .models import Task

def home(request):
    return render(request, 'hangarin/home.html')

def dashboard(request):
    tasks = Task.objects.all().order_by('deadline')
    return render(request, 'hangarin/dashboard.html', {'tasks': tasks})