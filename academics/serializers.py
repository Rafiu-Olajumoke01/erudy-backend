from rest_framework import serializers
from .models import ClassSession, ClassNote, Assignment, AssignmentSubmission, CapstoneGuideline


class ClassSessionSerializer(serializers.ModelSerializer):
    duration_hours = serializers.FloatField(read_only=True)

    class Meta:
        model = ClassSession
        fields = [
            'id', 'school', 'cohort', 'tutor', 'date',
            'start_time', 'end_time', 'topics_covered',
            'duration_hours', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        cohort = data.get('cohort', getattr(self.instance, 'cohort', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if cohort and school and cohort.school_id != school.id:
            raise serializers.ValidationError("This cohort does not belong to the selected school.")

        tutor = data.get('tutor', getattr(self.instance, 'tutor', None))
        if tutor and tutor.role != 'tutor':
            raise serializers.ValidationError({"tutor": "Selected user must have the role 'tutor'."})
        return data


class ClassNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassNote
        fields = [
            'id', 'school', 'session', 'title', 'content',
            'attachment', 'uploaded_by', 'created_at',
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at']

    def validate(self, data):
        session = data.get('session', getattr(self.instance, 'session', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if session and school and session.school_id != school.id:
            raise serializers.ValidationError("This session does not belong to the selected school.")
        return data


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id', 'school', 'cohort', 'title', 'description',
            'attachment', 'due_date', 'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate(self, data):
        cohort = data.get('cohort', getattr(self.instance, 'cohort', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if cohort and school and cohort.school_id != school.id:
            raise serializers.ValidationError("This cohort does not belong to the selected school.")
        return data


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'student', 'content',
            'attachment', 'submitted_at',
        ]
        read_only_fields = ['id', 'student', 'submitted_at']


class CapstoneGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapstoneGuideline
        fields = [
            'id', 'school', 'cohort', 'title', 'description',
            'requirements', 'attachment', 'deadline',
            'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate(self, data):
        cohort = data.get('cohort', getattr(self.instance, 'cohort', None))
        school = data.get('school', getattr(self.instance, 'school', None))
        if cohort and school and cohort.school_id != school.id:
            raise serializers.ValidationError("This cohort does not belong to the selected school.")
        return data