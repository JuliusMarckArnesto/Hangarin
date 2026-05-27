from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    category_name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class Priority(BaseModel):
    priority_level = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.priority_level
    
class Task(BaseModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=50,
         choices = [
             ("Pending", "Pending"),
             ("In Progress", "In Progress"),
             ("Completed", "Completed"),
         ], 
        default="pending")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask_title = models.CharField(max_length=150)
    subtask_status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
        ],
        default="pending")

    def __str__(self):
        return self.subtask_title
class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content #content[:50] returns the first 50 chracters