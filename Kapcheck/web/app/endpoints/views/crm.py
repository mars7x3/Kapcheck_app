from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db.models import PartnerProfile, Client, Payment, Payout, Task, Goal, CategoryPartner, Prize
from endpoints.serializers.crm import DashboardSerializer, CategoryPartnerSerializer, PartnerProfileSerializer, \
    ClientSerializer, PaymentSerializer, PayoutSerializer, GoalSerializer, PrizeSerializer, TaskSerializer, \
    PartnerProfileListSerializer, ClientListSerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=DashboardSerializer())
    def get(self, request):

        total_partners = PartnerProfile.objects.all().count()
        total_clients = Client.objects.all().count()
        total_payments = sum(
            Payment.objects.filter(is_paid=True)
            .values_list('amount', flat=True)
        )
        total_payouts = sum(
            Payout.objects.all()
            .values_list('amount', flat=True))
        pending_tasks = Task.objects.filter(is_done=False).count()
        active_goals = Goal.objects.filter(is_active=True).count()

        data = {
            "total_partners": total_partners,
            "total_clients": total_clients,
            "total_payments": total_payments,
            "total_payouts": total_payouts,
            "pending_tasks": pending_tasks,
            "active_goals": active_goals,
        }
        serializer = DashboardSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryPartnerView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CategoryPartner.objects.all()
    serializer_class = CategoryPartnerSerializer


class PartnerProfileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PartnerProfile.objects.all().select_related('category')
    serializer_class = PartnerProfileSerializer


class ClientView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all().select_related('partner')
    serializer_class = ClientSerializer


class PaymentView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all().select_related('client')
    serializer_class = PaymentSerializer


class PayoutView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payout.objects.all().select_related('partner')
    serializer_class = PayoutSerializer


class PrizeView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class GoalView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Goal.objects.all().prefetch_related('prizes')
    serializer_class = GoalSerializer


class TaskView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all().select_related('partner', 'client')
    serializer_class = TaskSerializer
