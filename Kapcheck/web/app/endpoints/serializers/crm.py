from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from db.models import CategoryPartner, PartnerProfile, Client, Payment, Payout, Goal, Prize, Task


class DashboardSerializer(serializers.Serializer):
    total_partners = serializers.IntegerField()
    total_clients = serializers.IntegerField()
    total_payments = serializers.DecimalField(max_digits=10,
                                              decimal_places=2)
    total_payouts = serializers.DecimalField(max_digits=10,
                                              decimal_places=2)
    pending_tasks = serializers.IntegerField()
    active_goals = serializers.IntegerField()


class CategoryPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPartner
        fields = ('id',
                  'title',
                  'percent',
                  'is_active')


class GetCategoryPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPartner
        fields = ('id',
                  'title')


class PartnerProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerProfile
        fields = ('id',
                  'fullname')


class PartnerProfileSerializer(serializers.ModelSerializer):
    category_info = SerializerMethodField(read_only=True)

    class Meta:
        model = PartnerProfile
        fields = ('id',
                  'fullname',
                  'phone',
                  'percent',
                  'is_individual',
                  'promo_code',
                  'requisites',
                  'telegram_id',
                  'payout_type',
                  'category',
                  'is_active',
                  'category_info')

    def get_category_info(self, obj):
        return GetCategoryPartnerSerializer(obj.category).data


class GetPartnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerProfile
        fields = ('id',
                  'fullname')


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id',
                  'fullname')


class ClientSerializer(serializers.ModelSerializer):
    partner_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = ('id',
                  'fullname',
                  'phone',
                  'status',
                  'partner',
                  'is_active',
                  'partner_info')

    def get_partner_info(self, obj):
        return GetPartnerProfileSerializer(obj.partner).data


class GetClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id',
                  'fullname')



class PaymentSerializer(serializers.ModelSerializer):
    client_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ('id',
                  'kapcheck_id',
                  'amount',
                  'is_paid',
                  'client',
                  'client_info')

    def get_client_info(self, obj):
        return GetClientSerializer(obj.client).data


class PayoutSerializer(serializers.ModelSerializer):
    partner_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Payout
        fields = ('id',
                  'amount',
                  'notes',
                  'partner',
                  'partner_info')

    def get_partner_info(self, obj):
        return GetPartnerProfileSerializer(obj.partner).data

    def create(self, validated_data):
        payout = Payout.objects.create(**validated_data)
        Payment.objects.filter(client__in=payout.partner.clients.all(),
                               is_paid=False).update(is_paid=True)
        return payout


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ('id',
                  'title',
                  'description',
                  'is_active')


class GetPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ('id',
                  'title')


class GoalSerializer(serializers.ModelSerializer):
    prizes_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Goal
        fields = ('id',
                  'title',
                  'start_date',
                  'end_date',
                  'target_amount',
                  'prizes',
                  'is_active',
                  'prizes_info')

    def get_prizes_info(self, obj):
        return GetPrizeSerializer(obj.prizes, many=True).data


class TaskSerializer(serializers.ModelSerializer):
    partner_info = SerializerMethodField(read_only=True)
    client_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ('id',
                  'description',
                  'is_done',
                  'date',
                  'partner',
                  'client',
                  'is_active',
                  'partner_info',
                  'client_info')

    def get_partner_info(self, obj):
        return GetPartnerProfileSerializer(obj.partner).data

    def get_client_info(self, obj):
        return GetClientSerializer(obj.client).data