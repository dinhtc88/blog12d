from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MemoryPost, Comment, FundTransaction, CalendarEvent, Notification, UserProfile

class UserSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='userprofile.display_name', read_only=True, allow_null=True)
    photoURL = serializers.CharField(source='userprofile.photo_url', read_only=True, allow_null=True)
    role = serializers.CharField(source='userprofile.role', read_only=True, allow_null=True)
    uid = serializers.CharField(source='userprofile.uid', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'displayName', 'photoURL', 'role', 'uid']

class UserProfileSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', required=False, allow_null=True)
    photoURL = serializers.CharField(source='photo_url', required=False, allow_null=True)
    joinedAt = serializers.DateTimeField(source='joined_at', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['uid', 'displayName', 'photoURL', 'email', 'role', 'joinedAt', 'birthday']

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'display_name' in mutable_data and 'displayName' not in mutable_data:
            mutable_data['displayName'] = mutable_data['display_name']
        if 'photo_url' in mutable_data and 'photoURL' not in mutable_data:
            mutable_data['photoURL'] = mutable_data['photo_url']
        if 'joined_at' in mutable_data and 'joinedAt' not in mutable_data:
            mutable_data['joinedAt'] = mutable_data['joined_at']
        return super().to_internal_value(mutable_data)

class MemoryPostSerializer(serializers.ModelSerializer):
    authorUid = serializers.CharField(source='author_uid_id')
    authorName = serializers.CharField(source='author_name')
    
    # Rất quan trọng: Phải cho phép các trường này null/không bắt buộc để khi Sửa bài không bị văng
    imageUrl = serializers.CharField(source='image_url', required=False, allow_null=True)
    imageUrls = serializers.JSONField(source='image_urls', required=False, allow_null=True)
    eventDate = serializers.CharField(source='event_date', required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)
    tags = serializers.JSONField(required=False, allow_null=True)
    
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isPublic = serializers.BooleanField(source='is_public', default=True)
    likedBy = serializers.JSONField(source='liked_by', required=False, allow_null=True)
    commentCount = serializers.IntegerField(source='comment_count', read_only=True)

    class Meta:
        model = MemoryPost
        fields = ['id', 'title', 'content', 'imageUrl', 'imageUrls', 'authorUid', 'authorName', 
                  'createdAt', 'tags', 'isPublic', 'type', 'eventDate', 'location', 'likes', 
                  'likedBy', 'commentCount']

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'author_uid' in mutable_data and 'authorUid' not in mutable_data:
            mutable_data['authorUid'] = mutable_data['author_uid']
        if 'author_name' in mutable_data and 'authorName' not in mutable_data:
            mutable_data['authorName'] = mutable_data['author_name']
        return super().to_internal_value(mutable_data)
class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post_id')
    authorUid = serializers.CharField(source='author_uid_id')
    authorName = serializers.CharField(source='author_name')
    authorPhotoURL = serializers.CharField(source='author_photo_url', required=False, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    parentCommentId = serializers.CharField(source='parent_comment_id', required=False, allow_null=True)
    replyToName = serializers.CharField(source='reply_to_name', required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'postId', 'authorUid', 'authorName', 'authorPhotoURL', 'content', 
                  'createdAt', 'parentCommentId', 'replyToName']

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'post_id' in mutable_data and 'postId' not in mutable_data:
            mutable_data['postId'] = mutable_data['post_id']
        if 'author_uid' in mutable_data and 'authorUid' not in mutable_data:
            mutable_data['authorUid'] = mutable_data['author_uid']
        if 'author_name' in mutable_data and 'authorName' not in mutable_data:
            mutable_data['authorName'] = mutable_data['author_name']
        if 'author_photo_url' in mutable_data and 'authorPhotoURL' not in mutable_data:
            mutable_data['authorPhotoURL'] = mutable_data['author_photo_url']
        if 'parent_comment_id' in mutable_data and 'parentCommentId' not in mutable_data:
            mutable_data['parentCommentId'] = mutable_data['parent_comment_id']
        if 'reply_to_name' in mutable_data and 'replyToName' not in mutable_data:
            mutable_data['replyToName'] = mutable_data['reply_to_name']
        return super().to_internal_value(mutable_data)

class FundTransactionSerializer(serializers.ModelSerializer):
    authorName = serializers.CharField(source='author_name')
    
    class Meta:
        model = FundTransaction
        fields = ['id', 'type', 'amount', 'description', 'date', 'authorName', 'details']

    # [BẢN FIX MỚI NHẤT]: Chốt chặn cho Quỹ lớp
    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'author_name' in mutable_data and 'authorName' not in mutable_data:
            mutable_data['authorName'] = mutable_data['author_name']
        return super().to_internal_value(mutable_data)

class NotificationSerializer(serializers.ModelSerializer):
    recipientUid = serializers.CharField(source='recipient_uid')
    senderName = serializers.CharField(source='sender_name')
    senderUid = serializers.CharField(source='sender_uid')
    targetId = serializers.CharField(source='target_id')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isRead = serializers.BooleanField(source='is_read', default=False)

    class Meta:
        model = Notification
        fields = ['id', 'recipientUid', 'senderName', 'senderUid', 'type', 'targetId', 'message', 'createdAt', 'isRead']

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'recipient_uid' in mutable_data and 'recipientUid' not in mutable_data:
            mutable_data['recipientUid'] = mutable_data['recipient_uid']
        if 'sender_name' in mutable_data and 'senderName' not in mutable_data:
            mutable_data['senderName'] = mutable_data['sender_name']
        if 'sender_uid' in mutable_data and 'senderUid' not in mutable_data:
            mutable_data['senderUid'] = mutable_data['sender_uid']
        if 'target_id' in mutable_data and 'targetId' not in mutable_data:
            mutable_data['targetId'] = mutable_data['target_id']
        return super().to_internal_value(mutable_data)

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'date', 'type', 'location', 'description']