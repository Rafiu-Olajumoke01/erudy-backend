from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'exam', 'application', 'score', 'remarks',
            'percentage', 'graded_by', 'graded_at',
        ]
        read_only_fields = ['id', 'graded_by', 'graded_at']

    def validate(self, data):
        exam = data.get('exam', getattr(self.instance, 'exam', None))
        application = data.get('application', getattr(self.instance, 'application', None))

        if exam and application and exam.school_id != application.school_id:
            raise serializers.ValidationError("This application does not belong to the same school as the exam.")

        if application and exam and application.cohort_id != exam.cohort_id:
            raise serializers.ValidationError(
                "This student is not enrolled in the cohort this exam belongs to."
            )

        score = data.get('score', getattr(self.instance, 'score', None))
        if score is not None and exam and score > exam.total_marks:
            raise serializers.ValidationError(
                {"score": f"Score cannot exceed the exam's total marks ({exam.total_marks})."}
            )

        return data