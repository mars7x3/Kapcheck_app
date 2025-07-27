from rest_framework import serializers


class BotPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10,
                                      decimal_places=2)
    is_paid = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class BotClientSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    phone = serializers.CharField()
    status = serializers.IntegerField()
    payments = BotPaymentSerializer(many=True)


class BotGetClientSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    phone = serializers.CharField()
    status = serializers.IntegerField()


class BotPartnerSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    phone = serializers.CharField()
    percent = serializers.DecimalField(max_digits=4,
                                       decimal_places=1)
    promo_code = serializers.CharField()
    telegram_id = serializers.CharField()
    requisites = serializers.CharField()
    payout_type = serializers.IntegerField()


class BotTaskSerializer(serializers.Serializer):
    description = serializers.CharField()
    is_done = serializers.BooleanField()
    client = BotGetClientSerializer()
    created_at = serializers.DateTimeField()


class BotPayoutSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10,
                                      decimal_places=2)
    notes = serializers.CharField()
    created_at = serializers.DateTimeField()


class BotPrizeSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class BotGoalSerializer(serializers.Serializer):
    title = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    target_amount = serializers.DecimalField(max_digits=10,
                                             decimal_places=2)
    completed_amount = serializers.DecimalField(max_digits=10,
                                                decimal_places=2)
    created_at = serializers.DateTimeField()
    prizes = BotPrizeSerializer(many=True)



class BotDashboardSerializer(serializers.Serializer):
    total_earnings = serializers.DecimalField(max_digits=10,
                                              decimal_places=2)
    total_clients = serializers.IntegerField()
    pending_amount = serializers.DecimalField(max_digits=10,
                                              decimal_places=2)
    pending_tasks = serializers.IntegerField()


class BotSerializer(serializers.Serializer):
    dashboard = BotDashboardSerializer()
    partner = BotPartnerSerializer()
    tasks = BotTaskSerializer(many=True)
    payouts = BotPayoutSerializer(many=True)
    clients = BotClientSerializer(many=True)
    goals = BotGoalSerializer(many=True)
