from datetime import datetime

from django.db import models
from django.db.models import Sum, F
from rest_framework import serializers

from .models import (
    Commission,
)
from apps.order.models import (
    OrderInvoicing,
)

from apps.accounts.models import (
    User,
)

from apps.accounts.serializers import (
    ProfileBasicSerializer,
    UserProfileSerializer,
)

from apps.client.serializers import (
    ClientNameSerializer,
)


class CommissionSerializer(serializers.ModelSerializer):
    owner_set = ProfileBasicSerializer(source='owner', read_only=True)

    class Meta:
        model = Commission
        fields = [
            'id',
            'owner',
            'owner_set',
            'invoicing',
            'commission_percentage',
            'notes',
            'status',
        ]

class CommissionInvoicingSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='commitment.order.contract.bidding.client.id',
                                   read_only=True)

    client_set = ClientNameSerializer(source='commitment.order.contract.bidding.client',
                                  read_only=True)

    commission_set = CommissionSerializer(source='commission_invoicing',
                                          read_only=True,
                                          many=True)

    date_delivery = serializers.CharField(source='delivery.date_delivery',
                                          read_only=True)

    invoicing_delivery_date = serializers.CharField(source='delivery.invoicing_delivery_date',
                                          read_only=True)

    delayed_days = serializers.SerializerMethodField()

    def get_delayed_days(self, obj):
        pay_date = obj.delivery.invoicing_delivery_date
        real_pay_date = obj.real_pay_date
        current_date = datetime.now().date()
        current_date = datetime(current_date.year, current_date.month, current_date.day)

        if pay_date:
            pay_date = datetime(pay_date.year, pay_date.month, pay_date.day)
        if real_pay_date:
            real_pay_date = datetime(real_pay_date.year, real_pay_date.month, real_pay_date.day)

        if real_pay_date and pay_date:
            diff = real_pay_date - pay_date

            if (diff.days < 0):
                return 0
            else:
                return diff.days
        elif pay_date and not real_pay_date:
            if pay_date > current_date:
                return 0
            else:
                diff = current_date - pay_date
                return diff.days
        else:
            return 0

    class Meta:
        model = OrderInvoicing
        fields = [
            'id',
            'delivery',
            'commitment',
            'note_number',
            'invoicing_date',
            'expected_payment_date',
            'real_pay_date',
            'annotation',
            'status',
            'situation',
            'client',
            'client_set',
            'commission_set',
            'date_delivery',
            'invoicing_delivery_date',
            'delayed_days',
            'commission_invoicing',
            'total_nf',
            'liquid_margin',
            'total_items',
        ]

class CommissionUserValuesSerializer(serializers.ModelSerializer):
    total_paid = serializers.SerializerMethodField()
    total_pending = serializers.SerializerMethodField()

    def get_total(self, obj, status):
        date_lte_str = self.context.get('date_lte')
        date_gte_str = self.context.get('date_gte')
        date_lte = datetime.strptime(date_lte_str, "%Y-%m-%d").date() if date_lte_str else None
        date_gte = datetime.strptime(date_gte_str, "%Y-%m-%d").date() if date_gte_str else None

        user = UserProfileSerializer(obj)
        owner_id = user.data['profile']['id']

        commission_filter = {
            'owner': owner_id,
            'status': status,
        }

        if date_gte:
            commission_filter['invoicing__real_pay_date__gte'] = date_gte

        if date_lte:
            commission_filter['invoicing__real_pay_date__lte'] = date_lte

        commissions_queryset = Commission.objects.filter(**commission_filter)

        total = 0

        if commissions_queryset.exists():
            total = commissions_queryset.aggregate(
                total_commission=Sum(
                    F('invoicing__delivery__items__item__item__price') *
                    F('invoicing__delivery__items__quantity') *
                    F('commission_percentage') / 100,
                    output_field=models.FloatField()
                )
            )['total_commission'] or 0

        return total

    def get_total_paid(self, obj):
        return self.get_total(obj, status='payed')

    def get_total_pending(self, obj):
        return self.get_total(obj, status='pending')

    class Meta:
        model = User
        fields = [
            'uuid',
            'total_paid',
            'total_pending',
        ]
