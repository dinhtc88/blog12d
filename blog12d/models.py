from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    display_name = models.CharField(max_length=255)
    photo_url = models.URLField(blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    birthday = models.CharField(max_length=10, blank=True, null=True) # DD/MM format
    
    def __str__(self):
        return self.display_name

class MemoryPost(models.Model):
    TYPE_CHOICES = (
        ('story', 'Story'),
        ('event', 'Event'),
        ('birthday', 'Birthday'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    
    # Tối ưu cho Postgres: Dùng ArrayField thay thế JSONField cho danh sách URL/String
    image_urls = ArrayField(models.URLField(max_length=1000), blank=True, default=list) 
    author_uid = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    author_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    tags = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    is_public = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='story')
    event_date = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    liked_by = ArrayField(models.CharField(max_length=255), blank=True, default=list) # Array of UIDs
    disliked_by = ArrayField(models.CharField(max_length=255), blank=True, default=list) # Array of UIDs
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(MemoryPost, on_delete=models.CASCADE, related_name='comments')
    author_uid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255)
    author_photo_url = models.URLField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment_id = models.CharField(max_length=255, blank=True, null=True)
    reply_to_name = models.CharField(max_length=255, blank=True, null=True)

class CalendarEvent(models.Model):
    TYPE_CHOICES = (
        ('event', 'Event'),
        ('birthday', 'Birthday')
    )
    title = models.CharField(max_length=255)
    date = models.DateField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class FundTransaction(models.Model):
    TYPE_CHOICES = (
        ('thu', 'Thu'),
        ('chi', 'Chi')
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=500)
    date = models.DateTimeField()
    author_name = models.CharField(max_length=255)
    
    # details có thể lưu dict phức tạp nên vẫn giữ nguyên JSONField
    details = models.JSONField(blank=True, default=list)

class Notification(models.Model):
    recipient_uid = models.CharField(max_length=255) # 'all' or user uid
    sender_name = models.CharField(max_length=255)
    sender_uid = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Tự động tạo UserProfile ngay khi User (auth_user) được tạo.
        # Sử dụng username làm 'uid' để khớp với logic ở Frontend của bạn.
        UserProfile.objects.create(
            uid=instance.username, 
            display_name=instance.username, 
            email=instance.email
        )

class LoginHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.display_name} - {self.timestamp}"