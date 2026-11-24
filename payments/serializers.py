from rest_framework import serializers
from django.utils import timezone
from .models import Payment, PromoCode, SubscriptionPayment

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            'id',
            'school',
            'code',
            'discount_percent',
            'is_active',
            'valid_until',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class PaymentInitiateSerializer(serializers.ModelSerializer):
    """Used by the applicant/student to initiate a payment for their application."""

    promo_code_input = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'school',
            'application',
            'amount',
            'payment_proof',
            'student_reference_note',
            'promo_code_input',
            'tx_ref',
            'status',
        ]
        read_only_fields = ['id', 'tx_ref', 'status']

    def validate(self, data):
        application = data.get('application')
        school = data.get('school')

        if application.school_id != school.id:
            raise serializers.ValidationError(
                "This application does not belong to the selected school."
            )

        course_fee = application.course.fee
        promo_input = data.pop('promo_code_input', None)
        promo = None

        if promo_input:
            try:
                promo = PromoCode.objects.get(school=school, code__iexact=promo_input)
            except PromoCode.DoesNotExist:
                raise serializers.ValidationError({"promo_code_input": "Invalid promo code for this school."})
            if not promo.is_valid:
                raise serializers.ValidationError({"promo_code_input": "This promo code is no longer valid."})

        expected_amount = course_fee
        if promo:
            discount = (course_fee * promo.discount_percent) / 100
            expected_amount = course_fee - discount

        data['amount'] = expected_amount
        data['promo_code'] = promo
        return data


class PaymentReviewSerializer(serializers.ModelSerializer):
    """Used by School Admin / Platform Owner to review and confirm a payment."""

    class Meta:
        model = Payment
        fields = [
            'id',
            'school',
            'application',
            'promo_code',
            'tx_ref',
            'amount',
            'confirmed_amount',
            'status',
            'payment_proof',
            'student_reference_note',
            'reviewed_by',
            'reviewed_at',
            'expires_at',
            'paid_at',
            'created_at',
        ]
        read_only_fields = [
            'id', 'school', 'application', 'promo_code', 'tx_ref',
            'amount', 'payment_proof', 'student_reference_note',
            'reviewed_by', 'reviewed_at', 'expires_at', 'created_at',
        ]

    def update(self, instance, validated_data):
        request = self.context['request']
        new_status = validated_data.get('status', instance.status)

        if new_status != instance.status and new_status == Payment.Status.PAID:
            validated_data['paid_at'] = timezone.now()

        if new_status != instance.status:
            validated_data['reviewed_by'] = request.user
            validated_data['reviewed_at'] = timezone.now()

        return super().update(instance, validated_data)


class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    """Used by the Platform Owner to view and confirm school subscription payments."""

    school_name = serializers.CharField(source='school.name', read_only=True)
    reference = serializers.CharField(source='tx_ref', read_only=True)

    class Meta:
        model = SubscriptionPayment
        fields = [
            'id',
            'school',
            'school_name',
            'plan',
            'amount',
            'confirmed_amount',
            'period_start',
            'period_end',
            'reference',
            'status',
            'method',
            'payment_proof',
            'reviewed_by',
            'reviewed_at',
            'paid_at',
            'created_at',
        ]
        read_only_fields = [
            'id', 'school', 'school_name', 'plan', 'amount',
            'period_start', 'period_end', 'reference', 'method',
            'payment_proof', 'reviewed_by', 'reviewed_at', 'paid_at', 'created_at',
        ]

    def update(self, instance, validated_data):
        request = self.context['request']
        new_status = validated_data.get('status', instance.status)

        if new_status != instance.status:
            validated_data['reviewed_by'] = request.user
            validated_data['reviewed_at'] = timezone.now()

            if new_status == SubscriptionPayment.Status.PAID:
                validated_data['paid_at'] = timezone.now()
                validated_data.setdefault('confirmed_amount', instance.amount)

        became_paid = (
            new_status != instance.status
            and new_status == SubscriptionPayment.Status.PAID
        )
        payment = super().update(instance, validated_data)

        if became_paid:
            school = payment.school
            school.subscription_plan = payment.plan
            school.subscription_status = 'active'
            if (
                not school.subscription_expires_at
                or payment.period_end > school.subscription_expires_at
            ):
                school.subscription_expires_at = payment.period_end
            school.save(update_fields=[
                'subscription_plan',
                'subscription_status',
                'subscription_expires_at',
            ])

        return payment