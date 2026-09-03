from rest_framework import serializers
from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'id', 'school', 'cohort', 'title', 'description',
            'total_marks', 'exam_date', 'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate(self, data):
        cohort = data.get('cohort', getattr(self.instance, 'cohort', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if cohort and school and cohort.school_id != school.id:
            raise serializers.ValidationError("This cohort does not belong to the selected school.")
        return data