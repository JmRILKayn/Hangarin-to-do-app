from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This ensures it's not created as a separate table [cite: 4431]

class Priority(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Priorities"  # Refactor for correct grammar [cite: 4091]

    def __str__(self):
        return self.name  # Add str method for each model [cite: 4070]

class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"  # Refactor for correct grammar [cite: 4091, 4096]

    def __str__(self):
        return self.name

class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="Pending"
    ) 
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class SubTask(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="Pending"
    )

    def __str__(self):
        return self.title

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"