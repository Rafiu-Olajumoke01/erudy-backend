from rest_framework import serializers
from .models import Application
from cohorts.models import Course, Cohort
from accounts.models import User
import secrets
import string

class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Used for the public application form — anyone can submit this, no login required."""

    class Meta:
        model = Application
        fields = [
            'id',
            'school',
            'course',
            'full_name',
            'email',
            'phone',
        ]
        read_only_fields = ['id']

    def validate(self, data):
        # Ensure the course actually belongs to the school being applied to
        if data['course'].school_id != data['school'].id:
            raise serializers.ValidationError(
                "This course does not belong to the selected school."
            )
        return data


class ApplicationSerializer(serializers.ModelSerializer):
    """Used by School Admin / Platform Owner to view and manage applications."""

    class Meta:
        model = Application
        fields = [
            'id',
            'school',
            'course',
            'full_name',
            'email',
            'phone',
            'status',
            'student',
            'cohort',
            'applied_at',
            'reviewed_at',
        ]
        read_only_fields = ['id', 'applied_at']

    def validate_student(self, value):
        if value and value.role != User.Role.STUDENT:
            raise serializers.ValidationError("Assigned student must have the 'student' role.")
        return value

    def validate(self, data):
        # If a cohort is being assigned, make sure it belongs to the same school as the application
        cohort = data.get('cohort') or getattr(self.instance, 'cohort', None)
        school = data.get('school') or getattr(self.instance, 'school', None)
        if cohort and school and cohort.school_id != school.id:
            raise serializers.ValidationError(
                "This cohort does not belong to the same school as the application."
            )
        return data

class ConvertToStudentSerializer(serializers.Serializer):
    cohort = serializers.PrimaryKeyRelatedField(queryset=Cohort.objects.all())

    def validate(self, data):
        application = self.context['application']

        if application.status != 'approved':
            raise serializers.ValidationError("Application must be approved before converting to a student.")

        if not application.payments.filter(status='paid').exists():
            raise serializers.ValidationError("Application has no confirmed payment yet.")

        if application.student is not None:
            raise serializers.ValidationError("This application has already been converted to a student account.")

        cohort = data['cohort']
        if cohort.school_id != application.school_id:
            raise serializers.ValidationError({"cohort": "This cohort does not belong to the same school as the application."})

        return data

    def save(self):
        application = self.context['application']
        cohort = self.validated_data['cohort']

        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))

        base_username = application.email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        student = User(
            username=username,
            email=application.email,
            first_name=application.full_name.split(' ')[0],
            last_name=' '.join(application.full_name.split(' ')[1:]) or '',
            role=User.Role.STUDENT,
            school=application.school,
        )
        student.set_password(temp_password)
        student.save()

        application.student = student
        application.cohort = cohort
        application.save()

        return {
            'username': username,
            'temporary_password': temp_password,
            'application_id': application.id,
            'cohort': cohort.name,
        }