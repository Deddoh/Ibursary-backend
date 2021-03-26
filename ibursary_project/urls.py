"""ibursary_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings 
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from rest_framework import routers
from ibursary_accounts.views import all_approved_applications, all_rejected_applications, under_review_applications, awardedApplicant,update_application_status,deleteapplicant, StudentDashboardView, AdminDashboardView, landing_page_view, get_applications, loggedUser, registered_applicants, new_application_submission, SubmittedApplicationsViewSet, TrialView, show_submissions, mresult, approve_reject

router = routers.DefaultRouter()
router.register(r'submittedforms', SubmittedApplicationsViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('ibursary_accounts.urls')),
    # path('applications/', get_applications),
    path('registered_members/', registered_applicants),
    path('is-logged-in/', loggedUser),
    path('awarded-applicant/', awardedApplicant),
    path('new_bursary_application/', new_application_submission),
    path('applications/', include(router.urls)),
    path('submissions/', show_submissions),
    # model test
    path('results/',mresult, name="results"),
    path('application-status/', approve_reject),

    # CRUD operations
    # DELETE
    path('deleteapplication/<int:id>/', csrf_exempt(deleteapplicant)),
    # UPDATE
    path('updateapplicationstatus/<int:id>/', update_application_status),

    # REPORT APIS
    # APPROVED
    path('sorted/', all_approved_applications),
    # REJECTED
    path('rejected/', all_rejected_applications),
    # UNDER REVIEW
    path('inprogress/', under_review_applications),

    url(r'bc-admin', login_required(AdminDashboardView.as_view()), name="bc-admin"),
    url(r'st-dashboard', login_required(StudentDashboardView.as_view()), name="st-dashboard"),
    url(r'home', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^.*', landing_page_view, name="welcome" ),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)