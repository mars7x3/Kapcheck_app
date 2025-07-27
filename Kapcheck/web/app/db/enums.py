from django.db import models


class UserStatusEnums(models.IntegerChoices):
    STAFF = 1, 'СОТРУДНИК'
    PARTNER = 2, 'ПАРТНЕР'


class PayoutEnums(models.IntegerChoices):
    M_BANK = 1, 'MBANK'
    O_DENGI = 2, 'O! ДЕНЬГИ'
    SIM_BANK = 3, 'SIM BANK'


class ClientStatusEnums(models.IntegerChoices):
    ACTIVE = 1, 'АКТИВНЫЙ'
    INACTIVE = 2, 'НЕАКТИВНЫЙ'


