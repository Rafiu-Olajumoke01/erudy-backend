from django.urls import path
from .views import (
    PaymentInitiateView,
    PaymentListView,
    PaymentReviewView,
    PromoCodeViewSet,
    SubscriptionPaymentListView,
    SubscriptionPaymentDetailView,
    SubscriptionPaymentStatsView,
)

urlpatterns = [
    path('payments/initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<uuid:pk>/', PaymentReviewView.as_view(), name='payment-review'),
    path('promo-codes/', PromoCodeViewSet.as_view(), name='promo-code-list'),
    path('subscription-payments/', SubscriptionPaymentListView.as_view(), name='subscription-payment-list'),
    path('subscription-payments/stats/', SubscriptionPaymentStatsView.as_view(), name='subscription-payment-stats'),
    path('subscription-payments/<int:pk>/', SubscriptionPaymentDetailView.as_view(), name='subscription-payment-detail'),
]