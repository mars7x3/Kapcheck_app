from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserStatusEnums, PayoutEnums, ClientStatusEnums


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class MyUser(AbstractUser):
    status = models.IntegerField(choices=UserStatusEnums.choices,
                                 null=True)


class CategoryPartner(BaseModel):
    title = models.CharField(max_length=30)
    percent = models.DecimalField(max_digits=4,
                                  decimal_places=1,
                                  default=0)


class StaffProfile(BaseModel):
    user = models.OneToOneField(MyUser,
                                on_delete=models.CASCADE,
                                related_name='s_profile')
    fullname = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)


class PartnerProfile(BaseModel):
    fullname = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    percent = models.DecimalField(max_digits=4,
                                  decimal_places=1,
                                  default=0)
    is_individual = models.BooleanField(default=False)
    promo_code = models.CharField(max_length=10)
    telegram_id = models.CharField(max_length=20)
    requisites = models.CharField(max_length=50)
    payout_type = models.IntegerField(choices=PayoutEnums.choices, null=True)
    category = models.ForeignKey(CategoryPartner,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='partners')


class Client(BaseModel):
    kapcheck_id = models.CharField(max_length=50)
    fullname = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    status = models.IntegerField(ClientStatusEnums.choices,
                                 null=True)
    partner = models.ForeignKey(PartnerProfile,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='clients')


class Payment(BaseModel):
    kapcheck_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2)
    is_paid = models.BooleanField(default=False)
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='payments')


class Payout(BaseModel):
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2)
    notes = models.TextField()
    partner = models.ForeignKey(PartnerProfile,
                                on_delete=models.CASCADE,
                                related_name='payouts')


class Prize(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField()


class Goal(BaseModel):
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    target_amount = models.DecimalField(max_digits=10,
                                        decimal_places=2)
    prizes = models.ManyToManyField(Prize,
                                    related_name='goals')


class PartnerGoal(BaseModel):
    goal = models.ForeignKey(Goal,
                             on_delete=models.CASCADE,
                             related_name='partners')
    partner = models.ForeignKey(PartnerProfile,
                             on_delete=models.CASCADE,
                             related_name='goals')


class Task(BaseModel):
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    partner = models.ForeignKey(PartnerProfile,
                                on_delete=models.CASCADE,
                                related_name='tasks')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='tasks')
