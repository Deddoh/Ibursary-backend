from django.urls import path
from . import views
from django.contrib.auth.decorators import permission_required, login_required

urlpatterns=[
    path('registert/', login_required(views.register), name='registert'),
    # display the applicant's registration page
    path('applicant_register/', (views.applicant_register.as_view()), name='applicant_register'),
    # applicant's login page
    path('login/',views.login_request, name='login'),
    path('logout/',views.logout_view, name='logout'),
    # class based view for the bursary application form
    path('apply_view/', views.TrialView.as_view(template_name="../templates/bursary_application_form.html"), name="apply_view"),
    path('test_submission/', views.bursary_form_application, name="test_submission"),
    # path('apply_view/', views.trial_form, name="apply_view")    
    # path('st-dashboard/', views.restricted_page.as_view(), name="st-dashboard")
]