from decimal import Decimal

from django.db.models import Sum
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from db.models import PartnerProfile, Task

from endpoints.serializers.tg_bot import BotSerializer

from db.models import Payment, Goal


class PartnerBotDataView(APIView):

    @extend_schema(responses=BotSerializer())
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        partner = PartnerProfile.objects.filter(telegram_id=telegram_id).first()
        if not partner:
            return Response({'text': 'Партнер с таким telegram_id не существует!'},
                            status=status.HTTP_400_BAD_REQUEST)

        clients = partner.clients.all()

        total_earnings = partner.payouts.aggregate(total=Sum('amount'))['total'] or 0
        pending_amount = (Payment.objects
                             .filter(client__partner=partner, is_paid=False)
                             .aggregate(total=Sum('amount'))['total']
                         ) or 0
        pending_amount = (pending_amount / Decimal('100') * partner.percent).quantize(Decimal('0.01'))

        total_clients = clients.count()
        pending_tasks = partner.tasks.filter(is_done=False).count()

        dashboard_data = {
            "total_earnings": total_earnings,
            "total_clients": total_clients,
            "pending_amount": pending_amount,
            "pending_tasks": pending_tasks
        }

        partner_data = {
            "fullname": partner.fullname,
            "phone": partner.phone,
            "percent": partner.percent,
            "promo_code": partner.promo_code,
            "telegram_id": partner.telegram_id,
            "requisites": partner.requisites,
            "payout_type": partner.payout_type,
        }

        tasks_data = [
            {
                "id": task.id,
                "description": task.description,
                "is_done": task.is_done,
                "client": {
                    "fullname": task.client.fullname,
                    "phone": task.client.phone,
                    "status": task.client.status
                },
                "created_at": task.created_at,
                "date": task.date
            }
            for task in partner.tasks.select_related('client').order_by('-created_at')
        ]

        payouts_data = [
            {
                "amount": payout.amount,
                "notes": payout.notes,
                "created_at": payout.created_at
            }
            for payout in partner.payouts.order_by('-created_at')
        ]

        clients_data = []
        for client in clients.prefetch_related('payments'):
            client_payments = [
                {
                    "kapcheck_id": payment.kapcheck_id,
                    "amount": payment.amount,
                    "is_paid": payment.is_paid,
                    "created_at": payment.created_at
                }
                for payment in client.payments.all()
            ]

            clients_data.append({
                "fullname": client.fullname,
                "phone": client.phone,
                "status": client.status,
                "payments": client_payments
            })

        goals = Goal.objects.filter(is_active=True)
        goals_data = []
        for pg in goals:

            total_payments = Payment.objects.filter(
                client__in=clients,
                created_at__date__gte=pg.start_date,
                created_at__date__lte=pg.end_date
            ).aggregate(total=Sum('amount'))['total'] or 0

            goal_data = {
                "title": pg.title,
                "start_date": pg.start_date,
                "end_date": pg.end_date,
                "target_amount": pg.target_amount,
                "completed_amount": total_payments,
                "created_at": pg.created_at,
                "prizes": [
                    {
                        "title": prize.title,
                        "description": prize.description,
                        "image": prize.image if prize.image else ''
                    } for prize in pg.prizes.all()
                ]
            }
            goals_data.append(goal_data)

        response_data = {
            "dashboard": dashboard_data,
            "partner": partner_data,
            "tasks": tasks_data,
            "payouts": payouts_data,
            "clients": clients_data,
            "goals": goals_data
        }

        serializer = BotSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskUpdateView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        task_id = request.data.get('task_id')

        partner = PartnerProfile.objects.filter(telegram_id=telegram_id).first()
        if not partner:
            return Response({'text': 'Партнер с таким telegram_id не существует!'},
                            status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.filter(id=task_id,
                                   partner=partner).first()
        if not task:
            return Response({'text': 'Задачи c такими данными не существует!'},
                            status=status.HTTP_400_BAD_REQUEST)

        task.is_done = True
        task.save()

        return Response('OK!',
                        status=status.HTTP_200_OK)