from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Task, CustomUser, TaskHistory, TaskCategory
from .serializers import TaskSerializer, CustomUserSerializer, TaskCategorySerializer, TaskHistorySerializer
from django.utils import timezone
from django.db.models import Q

# Create your views here.
#View for creating a new user
class CreateUserView(generics.CreateAPIView):
    model = CustomUser
    serializer_class = CustomUserSerializer

#View to list and create tasks
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return tasks belonging to the user or where the user is a collaborator
        return self.queryset.filter(Q(user=self.request.user) | Q(collaborators=self.request.user))
    
    def perform_create(self, serializer):
         # Save the task for the current user and handle collaborators
        serializer.save(user=self.request.user)

#View to retrieve, update, and delete tasks
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
# View to mark tasks as complete
class MarkTaskCompleteView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        task = serializer.instance
        task.mark_complete()

        # Log the completed task in history
        TaskHistory.objects.create(task=task, user=self.request.user, completed_at=timezone.now())

        if task.recurrence_interval != 'none':
            task.regenerate_task()  # Regenerate task if it's recurring

#Task categoty list/createview allows users to create and list their task categories.
class TaskCategoryListCreateView(generics.ListCreateAPIView):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only access their own categories
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure the category is created for the authenticated user
        serializer.save(user=self.request.user)



#retrives tha task completion history for the user
class TaskHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskHistory.objects.filter(user=self.request.user).order_by('-completed_at')

    

