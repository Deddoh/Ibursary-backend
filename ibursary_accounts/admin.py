from django.contrib import admin
from .models import User, BursaryApplicant, BursaryCommitteeAdmin, SubmittedApplicationsModel, NewApplicationModel, TrialModel
# Register your models here.

admin.site.register(User)
admin.site.register(BursaryApplicant)
admin.site.register(BursaryCommitteeAdmin)
admin.site.register(SubmittedApplicationsModel)
admin.site.register(NewApplicationModel)
admin.site.register(TrialModel)

