from rest_framework import serializers
from .models import Certificate
from accounts.models import User


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'id', 'school', 'student', 'file',
            'issued_date', 'uploaded_by', 'uploaded_at', 'updated_at',
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'updated_at']

    def validate_student(self, value):
        if value.role != User.Role.STUDENT:
            raise serializers.ValidationError("Certificates can only be issued to users with the 'student' role.")
        return value

    def validate(self, data):
        student = data.get('student', getattr(self.instance, 'student', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if student and school and student.school_id != school.id:
            raise serializers.ValidationError("This student does not belong to the selected school.")
        return data