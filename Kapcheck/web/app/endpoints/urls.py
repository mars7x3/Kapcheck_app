from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.crm import DashboardView, CategoryPartnerView, PartnerProfileView, ClientView, PaymentView, PayoutView, \
    PrizeView, GoalView, TaskView
from .views.tg_bot import PartnerBotDataView, TaskUpdateView
from .views.webhook import WHClientView, WHPaymentCreateView, WHExpiringView

router = DefaultRouter()

router.register('crm/partner/category', CategoryPartnerView)
router.register('crm/partner', PartnerProfileView)
router.register('crm/client', ClientView)
router.register('crm/payment', PaymentView)
router.register('crm/payout', PayoutView)
router.register('crm/prize', PrizeView)
router.register('crm/goal', GoalView)
router.register('crm/task', TaskView)



urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include([
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

        path('tgbot/data/', PartnerBotDataView.as_view()),
        path('tgbot/task/update/', TaskUpdateView.as_view()),


        path('crm/dashboard/', DashboardView.as_view()),

        path('wh/client/', WHClientView.as_view()),
        path('wh/payment/', WHPaymentCreateView.as_view()),
        path('wh/expiring/', WHExpiringView.as_view()),



        path('', include(router.urls)),
    ])),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
