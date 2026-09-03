from rest_framework import serializers
from .models import Announcement, Message
from accounts.models import User


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id', 'school', 'title', 'content', 'audience',
            'posted_by', 'created_at',
        ]
        read_only_fields = ['id', 'posted_by', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'school', 'sender', 'recipient', 'subject',
            'content', 'parent', 'is_warning', 'is_read', 'created_at',
        ]
        read_only_fields = ['id', 'sender', 'created_at']

    def validate(self, data):
        recipient = data.get('recipient')
        school = data.get('school', getattr(self.instance, 'school', None))

        if recipient and school and recipient.school_id != school.id and recipient.role != User.Role.PLATFORM_OWNER:
            raise serializers.ValidationError("Recipient does not belong to the selected school.")

        parent = data.get('parent')
        if parent and school and parent.school_id != school.id:
            raise serializers.ValidationError("Reply must belong to the same school as the original message.")

        return data