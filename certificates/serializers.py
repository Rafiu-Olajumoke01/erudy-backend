from rest_framework import serializers
from .models import Certificate
from accounts.models import User


class CertificateSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    student_name = serializers.SerializerMethodField()
    student_email = serializers.CharField(source='student.email', read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    cohort_name = serializers.SerializerMethodField()
    class Meta:
        model = Certificate
        fields = [
            'id', 'school', 'student', 'file',
            'issued_date', 'uploaded_by', 'uploaded_at', 'updated_at',
            'school_name', 'student_name', 'student_email',
            'uploaded_by_name', 'course_name', 'cohort_name',
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

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username

    def get_uploaded_by_name(self, obj):
        if not obj.uploaded_by:
            return None
        return obj.uploaded_by.get_full_name() or obj.uploaded_by.username

    def _application(self, obj):
        return (
            obj.student.applications
            .select_related('course', 'cohort')
            .filter(cohort__isnull=False)
            .first()
        )

    def get_course_name(self, obj):
        app = self._application(obj)
        return app.course.name if app else None

    def get_cohort_name(self, obj):
        app = self._application(obj)
        return app.cohort.name if app else None