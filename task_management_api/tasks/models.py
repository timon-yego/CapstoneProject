from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)
    

#CustomUser model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True) 
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    
#Task category definition
class TaskCategory(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# Task model definition
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Reference to CustomUser
    category = models.ForeignKey(TaskCategory, null=True, blank=True, on_delete=models.SET_NULL)
    recurrence_interval = models.CharField(
        max_length=10,
        choices=[('none', 'None'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='none'
    )
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborative_tasks', blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


    def mark_complete(self):
        """Mark the task as completed and set the timestamp."""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        """Revert the task to incomplete status."""
        self.status = 'pending'
        self.completed_at = None
        self.save()
       
    
    def regenerate_task(self):
        """Regenerate a recurring task after it's completed."""
        if self.recurrence_interval == 'daily':
            self.due_date = self.due_date + timezone.timedelta(days=1)
        elif self.recurrence_interval == 'weekly':
            self.due_date = self.due_date + timezone.timedelta(weeks=1)
        elif self.recurrence_interval == 'monthly':
            self_due_date = self.due_date + timezone.timedelta(weeks=4)
        self.status = 'pending'
        self.completed_at = None
        self.save()

    def __str__(self):
        return self.title
    
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_at = models.DateTimeField()

    def __str__(self):
        return f"History of {self.task.title}"