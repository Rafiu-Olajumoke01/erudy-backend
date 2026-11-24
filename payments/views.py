from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment, PromoCode, SubscriptionPayment
from .serializers import (
    PaymentInitiateSerializer,
    PaymentReviewSerializer,
    PromoCodeSerializer,
    SubscriptionPaymentSerializer,
)
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

class IsPlatformOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.PLATFORM_OWNER


class SubscriptionPaymentListView(generics.ListAPIView):
    """Platform Owner only — every subscription payment schools have made to Edworth."""
    serializer_class = SubscriptionPaymentSerializer
    permission_classes = [IsPlatformOwner]

    def get_queryset(self):
        qs = SubscriptionPayment.objects.select_related('school')
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')

        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                Q(school__name__icontains=search)
                | Q(tx_ref__icontains=search)
                | Q(plan__icontains=search)
            )
        return qs


class SubscriptionPaymentDetailView(generics.RetrieveUpdateAPIView):
    """Platform Owner confirms or fails a subscription payment (PATCH status)."""
    queryset = SubscriptionPayment.objects.select_related('school')
    serializer_class = SubscriptionPaymentSerializer
    permission_classes = [IsPlatformOwner]


class SubscriptionPaymentStatsView(APIView):
    """Numbers for the four cards on /hq/payments."""
    permission_classes = [IsPlatformOwner]

    def get(self, request):
        qs = SubscriptionPayment.objects.all()
        S = SubscriptionPayment.Status
        collected = qs.filter(status=S.PAID).aggregate(
            total=Sum(Coalesce('confirmed_amount', 'amount'))
        )['total']

        return Response({
            'total_collected': collected or 0,
            'total_count': qs.count(),
            'paid_count': qs.filter(status=S.PAID).count(),
            'awaiting_count': qs.filter(status=S.AWAITING_CONFIRMATION).count(),
            'pending_count': qs.filter(status=S.PENDING).count(),
            'failed_count': qs.filter(status=S.FAILED).count(),
        })