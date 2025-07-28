from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db.models import PartnerProfile, Client, Payment, Task
from endpoints.serializers.webhook import WHExpiringSerializer, WHClientSerializer, WHPaymentSerializer


class WHClientView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(request=WHClientSerializer())
    def post(self, request):
        serializer = WHClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        client = Client.objects.filter(kapcheck_id=validated_data.get('client_id')).first()
        if client:
            client.fullname = validated_data.get('client_fullname')
            client.phone = validated_data.get('client_phone')
            client.save()
        else:
            promo_code = validated_data.get('client_promo_code')
            partner = PartnerProfile.objects.filter(promo_code=promo_code).first()
            if not partner:
                return Response({'detail': 'По промокоду не найден партнер!'},
                                status=status.HTTP_400_BAD_REQUEST)

            Client.objects.create(kapcheck_id=validated_data.get('client_id'),
                                  fullname=validated_data.get('client_fullname'),
                                  phone=validated_data.get('client_phone'),
                                  partner=partner)

        return Response({'detail': 'OK'},
                        status=status.HTTP_200_OK)


class WHPaymentCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(request=WHPaymentSerializer())
    def post(self, request):
        serializer = WHPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        client = Client.objects.filter(kapcheck_id=validated_data.get('client_id')).first()
        if not client:
            return Response({'detail': 'Нет такого клиента!'},
                            status=status.HTTP_400_BAD_REQUEST)

        Payment.objects.create(kapcheck_id=validated_data.get('payment_id'),
                               amount=validated_data.get('amount'),
                               client=client)

        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)


class WHExpiringView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(request=WHExpiringSerializer())
    def post(self, request):
        serializer = WHExpiringSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        client = Client.objects.filter(kapcheck_id=validated_data.get('client_id')).first()
        if not client:
            return Response({'detail': 'Нет такого клиента!'},
                            status=status.HTTP_400_BAD_REQUEST)

        Task.objects.create(client=client,
                            partner=client.partner,
                            description='До окончания тарифа осталось 3 дня. Сообщите клиенту.')

        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)


