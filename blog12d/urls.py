from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, MemoryPostViewSet, CommentViewSet,
    CalendarEventViewSet, FundTransactionViewSet, NotificationViewSet,
    LoginHistoryViewSet
)

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', MemoryPostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'events', CalendarEventViewSet)
router.register(r'funds', FundTransactionViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'login-history', LoginHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
