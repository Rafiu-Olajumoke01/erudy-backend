from rest_framework import serializers
from .models import School
from cohorts.models import Course


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id',
            'name',
            'slug',
            'email',
            'phone',
            'address',
            'logo',
            'subscription_plan',
            'subscription_status',
            'subscription_expires_at',
            'is_active',
            'date_onboarded',
        ]
        read_only_fields = ['id', 'slug', 'date_onboarded']


class PublicSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'name', 'slug', 'logo']


class PublicCourseSerializer(serializers.ModelSerializer):
    """Courses a visitor can pick from on the school's public Apply form."""

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'duration_weeks', 'fee']