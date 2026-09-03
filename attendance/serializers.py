from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id', 'session', 'application', 'status',
            'marked_by', 'marked_at',
        ]
        read_only_fields = ['id', 'marked_by', 'marked_at']

    def validate(self, data):
        session = data.get('session', getattr(self.instance, 'session', None))
        application = data.get('application', getattr(self.instance, 'application', None))

        if session and application and session.school_id != application.school_id:
            raise serializers.ValidationError(
                "This application does not belong to the same school as the session."
            )

        if application and application.cohort_id != (session.cohort_id if session else None):
            raise serializers.ValidationError(
                "This student is not enrolled in the cohort this session belongs to."
            )

        return data


class BulkAttendanceEntrySerializer(serializers.Serializer):
    application = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Attendance.STATUS_CHOICES)


class BulkAttendanceSerializer(serializers.Serializer):
    """Used to mark attendance for an entire session's roster in one request."""
    session = serializers.IntegerField()
    entries = BulkAttendanceEntrySerializer(many=True)