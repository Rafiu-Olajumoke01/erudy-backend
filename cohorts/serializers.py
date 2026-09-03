from rest_framework import serializers

from .models import Course, Cohort


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'school',
            'name',
            'description',
            'duration_weeks',
            'fee',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class CohortSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cohort
        fields = [
            'id',
            'school',
            'course',
            'name',
            'tutor',
            'start_date',
            'end_date',
            'status',
            'is_active',
            'student_count',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_tutor(self, value):
        if value is not None and value.role != 'tutor':
            raise serializers.ValidationError(
                "Selected user must have the role 'tutor'."
            )
        return value

    def validate(self, data):
        school = data.get('school', getattr(self.instance, 'school', None))
        course = data.get('course', getattr(self.instance, 'course', None))

        if school and course and course.school_id != school.id:
            raise serializers.ValidationError(
                {"course": "This course does not belong to the selected school."}
            )
        return data