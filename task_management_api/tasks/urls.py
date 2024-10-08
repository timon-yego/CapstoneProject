from django.urls import path
from .views import TaskListCreateView, TaskDetailView, MarkTaskCompleteView, CreateUserView, TaskCategoryListCreateView, TaskHistoryListView
from .views import UserListView, UserDetailView, UserRegistrationView


urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/complete/', MarkTaskCompleteView.as_view(), name='task-complete'),
    path('users/create/', CreateUserView.as_view(), name='create-user'),
    path('categories/', TaskCategoryListCreateView.as_view(), name='category-list-create'),
    path('history/', TaskHistoryListView.as_view(), name='task-history-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]