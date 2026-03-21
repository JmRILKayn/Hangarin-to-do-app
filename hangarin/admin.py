from django.contrib import admin
from .models import Priority, Category, Task, SubTask, Note

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',) # Display just the name field [cite: 57]
    search_fields = ('name',) # Make it searchable [cite: 57]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) # Display just the name field [cite: 57]
    search_fields = ('name',) # Make it searchable [cite: 57]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Display title, status, deadline, priority, category [cite: 47]
    list_display = ('title', 'status', 'deadline', 'priority', 'category') 
    # Add filters for status, priority, category [cite: 48]
    list_filter = ('status', 'priority', 'category')
    # Enable search on title and description [cite: 49]
    search_fields = ('title', 'description')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # Display title, status, and a custom field parent_task_name [cite: 51, 52]
    list_display = ('title', 'status', 'parent_task')
    # Filter by status [cite: 53]
    list_filter = ('status',)
    # Enable search on title [cite: 54]
    search_fields = ('title',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Display task, content, and created_at [cite: 59]
    list_display = ('task', 'content', 'created_at')
    # Filter by created_at [cite: 60]
    list_filter = ('created_at',)
    # Enable search on content [cite: 61]
    search_fields = ('content',)