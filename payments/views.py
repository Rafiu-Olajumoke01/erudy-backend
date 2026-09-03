from rest_framework import generics, permissions
from .models import Payment, PromoCode
from .serializers import PaymentInitiateSerializer, PaymentReviewSerializer, PromoCodeSerializer
from accounts.models import User


class IsPlatformOwnerOrSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN]
        )


class PaymentInitiateView(generics.CreateAPIView):
    """Public — applicant initiates payment for their (approved) application, no login required."""
    queryset = Payment.objects.all()
    serializer_class = PaymentInitiateSerializer
    permission_classes = [permissions.AllowAny]


class PaymentListView(generics.ListAPIView):
    """School Admin sees only their school's payments; Platform Owner sees all."""
    serializer_class = PaymentReviewSerializer
    permission_classes = [IsPlatformOwnerOrSchoolAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Payment.objects.all()
        return Payment.objects.filter(school=user.school)


class PaymentReviewView(generics.RetrieveUpdateAPIView):
    """School Admin/Platform Owner reviews a payment — confirm, set confirmed_amount, mark paid/failed."""
    serializer_class = PaymentReviewSerializer
    permission_classes = [IsPlatformOwnerOrSchoolAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Payment.objects.all()
        return Payment.objects.filter(school=user.school)


class PromoCodeViewSet(generics.ListCreateAPIView):
    """School Admin/Platform Owner manages promo codes for their school."""
    serializer_class = PromoCodeSerializer
    permission_classes = [IsPlatformOwnerOrSchoolAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return PromoCode.objects.all()
        return PromoCode.objects.filter(school=user.school)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)