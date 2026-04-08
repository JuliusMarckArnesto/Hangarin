from django.contrib import admin
from .models import Priority, Category, Task, SubTask, Note

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)
    search_fields = ("category_name",)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("priority_level",)
    search_fields = ("priority_level",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "deadline", 
                    "priority", "category",)
    list_filter = ("status", "priority", "category",)
    search_display = ("title", "description",)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("subtask_title", "subtask_status", "parent_task_name",)
    list_filter = ("subtask_status",)
    search_fields = ("subtask_title",)

    def parent_task_name(self, obj):
        if obj.parent_task:
            return obj.parent_task.title
        return "No Parent"

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "content", "created_at",)
    list_filter = ("created_at",)
    search_fields = ("content",)