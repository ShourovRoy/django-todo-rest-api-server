from django.db import models
from accounts.models import MyUser
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class TodoModel(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)


    def __str__(self):
        return self.title


