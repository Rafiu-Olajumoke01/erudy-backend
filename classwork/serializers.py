from rest_framework import serializers
from .models import Classwork, ClassworkSubmission


class ClassworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classwork
        fields = [
            'id', 'school', 'cohort', 'session', 'title',
            'instructions', 'attachment', 'posted_by', 'created_at',
        ]
        read_only_fields = ['id', 'posted_by', 'created_at']

    def validate(self, data):
        cohort = data.get('cohort', getattr(self.instance, 'cohort', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if cohort and school and cohort.school_id != school.id:
            raise serializers.ValidationError("This cohort does not belong to the selected school.")

        session = data.get('session', getattr(self.instance, 'session', None))
        if session and cohort and session.cohort_id != cohort.id:
            raise serializers.ValidationError({"session": "This session does not belong to the selected cohort."})

        return data


class ClassworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassworkSubmission
        fields = [
            'id', 'classwork', 'student', 'content',
            'attachment', 'submitted_at',
        ]
        read_only_fields = ['id', 'student', 'submitted_at']