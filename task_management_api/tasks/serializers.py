from rest_framework import serializers
from .models import Task, CustomUser, TaskCategory, TaskHistory

#Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user

class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ['id', 'name', 'user']
        
#Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    collaborators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), write_only=True
    )  # Add collaborators by ID
    collaborator_emails = serializers.StringRelatedField(source='collaborators', many=True, read_only=True)
    category = TaskCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskCategory.objects.all(), source='category', write_only=True, allow_null=True
    )  # Create/update task with category


    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'priority_level', 'status',
            'collaborators', 'collaborator_emails',
            'category', 'category_id','completed_at'
        ]
    
    def create(self, validated_data):
        collaborators = validated_data.pop('collaborators', [])
        task = super().create(validated_data)
        task.collaborators.set(collaborators) # Assign collaborators
        return task

    def update(self, instance, validated_data):
        collaborators = validated_data.pop('collaborators', [])
        task = super().update(instance, validated_data)
        task.collaborators.set(collaborators)  # Update collaborators
        return task


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = ['id', 'task', 'user', 'completed_at']


    