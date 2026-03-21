from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task

def home(request):
    return render(request, 'hangarin/home.html')

@login_required
def dashboard(request):
    tasks = Task.objects.all().order_by('deadline')
    return render(request, 'hangarin/dashboard.html', {'tasks': tasks})