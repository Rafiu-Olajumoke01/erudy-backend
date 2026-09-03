from rest_framework import serializers
from .models import School


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
            'is_active',
            'date_onboarded',
        ]
        read_only_fields = ['id', 'slug', 'date_onboarded']