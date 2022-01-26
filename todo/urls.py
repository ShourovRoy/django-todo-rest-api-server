from django.urls import path
from .views import TodoView, TodoDetailView

urlpatterns = [
    path('todolist', TodoView.as_view(), name='todoList'),
    path('todo/<int:pk>', TodoDetailView.as_view(), name='todoDetail'),
]