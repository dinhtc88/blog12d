from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from .models import UserProfile, MemoryPost, Comment, CalendarEvent, FundTransaction, Notification, LoginHistory
from .serializers import (
    UserProfileSerializer, MemoryPostSerializer, CommentSerializer,
    CalendarEventSerializer, FundTransactionSerializer, NotificationSerializer, LoginHistorySerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        
        # Kiểm tra đăng nhập
        if not user or not user.is_authenticated:
            return Response({"message": "Vui lòng đăng nhập để thực hiện!"}, status=status.HTTP_401_UNAUTHORIZED)
            
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        
        # Kiểm tra mật khẩu cũ
        if not user.check_password(old_password):
            return Response({"message": "Mật khẩu hiện tại không chính xác!"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Đặt mật khẩu mới và lưu lại
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "Đổi mật khẩu thành công!"}, status=status.HTTP_200_OK)

class MemoryPostViewSet(viewsets.ModelViewSet):
    queryset = MemoryPost.objects.all().order_by('-created_at')
    serializer_class = MemoryPostSerializer
    def perform_destroy(self, instance):
        post_id = str(instance.id)
        from .models import Notification
        Notification.objects.filter(target_id=post_id).delete()
        super().perform_destroy(instance)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user_uid = request.user.username 
        
        if not user_uid:
            return Response({"detail": "Chưa đăng nhập"}, status=status.HTTP_401_UNAUTHORIZED)

        liked_by = post.liked_by if post.liked_by else []

        # XÓA BỎ IF ELSE KIỂM TRA TRÙNG LẶP
        # Luôn luôn thêm user vào danh sách và cộng 1 tim
        liked_by.append(user_uid)
        post.likes = (post.likes or 0) + 1

        post.liked_by = liked_by
        post.save()

        return Response({
            "detail": "Đã thả tim",
            "likes": post.likes,
            "likedBy": post.liked_by
        }, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all().order_by('date')
    serializer_class = CalendarEventSerializer

class FundTransactionViewSet(viewsets.ModelViewSet):
    queryset = FundTransaction.objects.all().order_by('-date')
    serializer_class = FundTransactionSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    @action(detail=True, methods=['post'], url_path='mark_read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Thành công"})

class LoginHistoryViewSet(viewsets.ModelViewSet):
    queryset = LoginHistory.objects.all().order_by('-timestamp')
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            profile = UserProfile.objects.get(uid=user.username)
            if profile.role == 'admin':
                return LoginHistory.objects.all().order_by('-timestamp')
        except UserProfile.DoesNotExist:
            pass
        return LoginHistory.objects.none()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        request = self.context.get('request')
        ip_address = None
        user_agent = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')
        
        try:
            profile = UserProfile.objects.get(uid=user.username)
            LoginHistory.objects.create(
                user=profile,
                ip_address=ip_address,
                user_agent=user_agent
            )
        except Exception as e:
            print("Error creating login history:", e)
            pass

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
