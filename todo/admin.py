from django.contrib import admin
from .models import (
    Category,
    TodoModel
)
# Register your models here.


admin.site.register(Category)
admin.site.register(TodoModel)