from rest_framework import serializers


class WHClientCreateSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    client_fullname = serializers.CharField()
    client_phone = serializers.CharField()
    client_promo_code = serializers.CharField()


class WHPaymentSerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10,
                                      decimal_places=2)
    client_id = serializers.CharField()


class WHExpiringSerializer(serializers.Serializer):
    client_id = serializers.CharField()


