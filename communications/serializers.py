from rest_framework import serializers
from .models import Announcement, Message
from accounts.models import User


class AnnouncementSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    posted_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = [
            'id', 'school', 'school_name', 'title', 'content', 'audience',
            'posted_by', 'posted_by_name', 'created_at',
        ]
        read_only_fields = ['id', 'posted_by', 'created_at']

    def get_posted_by_name(self, obj):
        u = obj.posted_by
        return (u.get_full_name() or u.email) if u else None


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