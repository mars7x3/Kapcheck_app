from django.contrib import admin

from db.models import *

admin.site.register(MyUser)
admin.site.register(CategoryPartner)
admin.site.register(StaffProfile)
admin.site.register(PartnerProfile)
admin.site.register(Client)
admin.site.register(Payment)
admin.site.register(Payout)
admin.site.register(Prize)
admin.site.register(Goal)
admin.site.register(PartnerGoal)
admin.site.register(Task)


