from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ParentStudentLink

User = get_user_model()


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ParentStudentLinkSerializer(serializers.ModelSerializer):
    student_detail = ChildSerializer(source='student', read_only=True)

    class Meta:
        model = ParentStudentLink
        fields = ['id', 'parent', 'student', 'student_detail', 'relationship', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        request = self.context['request']
        parent = attrs['parent']
        student = attrs['student']

        if parent.role != 'parent':
            raise serializers.ValidationError("The parent user must have the Parent role.")
        if student.role != 'student':
            raise serializers.ValidationError("The student user must have the Student role.")
        if parent.school_id != student.school_id:
            raise serializers.ValidationError("Parent and student must belong to the same school.")
        if request.user.role == 'school_admin' and parent.school_id != request.user.school_id:
            raise serializers.ValidationError("You can only link users in your own school.")

        return attrs