from django.urls import path
from .views import TaskListCreateView, TaskDetailView, MarkTaskCompleteView, CreateUserView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
     path('tasks/<int:pk>/complete/', MarkTaskCompleteView.as_view(), name='task-complete'),
    path('users/create/', CreateUserView.as_view(), name='create-user'),
]