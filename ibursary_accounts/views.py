from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status
from rest_framework import viewsets, permissions
from . import serializers
from django.core.exceptions import PermissionDenied
# from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views import View
from django.template import RequestContext
# from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView
from .models import User, BursaryApplicant, BursaryCommitteeAdmin, SubmittedApplicationsModel, NewApplicationModel, TrialModel
from .form import ApplicantSignUpForm, BursaryAdminSignUpForm, NewApplicationForm, TrialApplicationForm
from .serializers import SubmittedApplicationsModelSerializer, BursaryApplicantSerializer, NewApplicationSerializer, UserSerializer, TrialModelSerializer
from django.views.decorators.csrf import csrf_exempt

# ########################################## machine learning model ######################################
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score





def get_predictions(  number_of_siblings, total_fee, paid, outstanding_balance, father_gross_income, mother_gross_income, guardian_gross_income):
    cls = joblib.load('deployed_model.sav')
    prediction = cls.predict( number_of_siblings, total_fee, paid, outstanding_balance, father_gross_income, mother_gross_income, guardian_gross_income)

    if prediction == 0:
        return "not awarded"
    elif prediction == 1:
        return "AWARDED"
    else:
        return "ERROR"

def approve_reject(unit):
    # try:
        ml_model = joblib.load('ibursary_fundmodel.sav')
        scaler = joblib.load('scalers.pkl')
            # mydata = request.data
            # unit = np.array(list(mydata.values()))

        sc = MinMaxScaler()
        # X_train = sc_x.fit_transform(X_train)
        X_test = scaler.transform(unit)

        # df_test = pd.DataFrame(unit)
        # b = sc_x.fit_transform(df_test)
        # X = sc_x.transform(unit)


            # scalers = joblib.load('scalers.pkl') 
            # X = scalers.transform(unit)
        y_pred = ml_model.predict(X_test)
        # y_pred = (y_pred>0.58)
        newdf = pd.DataFrame(y_pred, columns=['Application_Status'])
        newdf=newdf.replace({1:'Approve application', 0:'Reject application'})
        # return ('Application status: {}'.format(newdf))
        return(newdf)
    # except ValueError as e:
        # return HttpResponse(e.args[0], status.HTTP_400_BAD_REQUEST)

def ohevalue(df):

    ohe_col = ['disability_0.0', 'disability_1.0','employed_No', 'employed_Yes','gender_Female', 'gender_Male','outstanding_balance_log','number_of_siblings', 'school_type', 'paid', 'father_gross_income',
       'outstanding_balance', 'total_fee', 
        'benefitted_No', 'benefitted_Yes',
        
       'status_both_parents_alive', 'status_partial_orphan',
       'status_total_orphan']
    cat_columns=['gender','school_type', 'benefitted','disability','status']
    df_processed = pd.get_dummies(df, prefix_sep="_", columns=cat_columns)
    newdict={}
    for i in ohe_col:
        if i in df_processed.columns:
            newdict[i]=df_processed[i].values
        else:
            newdict[i]=0
    newdf=pd.DataFrame(newdict, index=[0])
    return newdf

def mresult(request):

    if request.method == 'POST':
        form=TrialApplicationForm(request.POST)
        if form.is_valid():
            # convert form data into a dictionary
            myDict = (request.POST).dict()
        # read the dict as a dataframe
            df = pd.DataFrame(myDict, index=[0])
            print(approve_reject(ohevalue(df)))
            print("Hot Encoded", ohevalue(df))
            print("Raw values", df)
           
            answer = approve_reject(ohevalue(df))
            
            Xscalers = approve_reject(ohevalue(df))
            messages.success(request, 'Recommendation: {}'.format(answer))
    
    form = TrialApplicationForm()
    return render(request, '../templates/bursary_application_form.html', {'form': form})
            
            







  



#  result = get_predictions(number_of_siblings, total_fee, paid, outstanding_balance, father_gross_income, mother_gross_income, guardian_gross_income)
  
  

    # result = cls.predict([indv])
    # for i in result:
    #     if result == 1:
    #         print ("AWARDED 10000")
    #     elif result == 2:
    #         print("AWARDED 5000")
    #     elif result == 3:
    #         print("AWARDED 5000")
    #     elif result == 4:
    #         print("AWARDED 5000")
    #     else:
    #         print("You are not eligible for a bursary at this time")


    # print(indv)
    # print("The predicted class is: ", result)


    # return JsonResponse({'message': 'result successful'})
    


# Create your views here.
# def apply_for_bursary(request):
#     return render(request, '../templates/bursary_application_form.html')

def register(request):
    return render(request, '../templates/applicant_registration.html')

# a view that displays a form for creating the object then saves the object
# @csrf_exempt
class applicant_register(CreateView):
    model = User
    # form name from form.py
    form_class = ApplicantSignUpForm
    template_name = '../templates/student_registration.html'

    # send an email verification to a new user's email address

    # redirect to login page after successfully saving  a new user(applicant) to database 
    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('/accounts/login/')



def landing_page_view(request):
    # template_name = "../templates/landing_page.html"
    return render(request, "../templates/landing_page.html")

# restrict access to any page on the admin dashboard if not logged in
class AdminDashboardView(TemplateResponseMixin, ContextMixin, View):
    template_name = "../templates/home.html"

    def get(self, request, **kwargs):
        try:
            current_user = request.user
            if current_user.is_bursarycommitteeadmin == True and current_user.is_authenticated and (bool(request.path_info == '/') or bool(request.path_info == '/accounts/login/')):
                return redirect("/bc-admin/")
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

#############################################################################
# restrict access to any page on the student dashboard if not logged in
class StudentDashboardView(TemplateResponseMixin, ContextMixin, View):
    # template containing the frontend app
    template_name="../templates/home.html"

    def get(self, request, **kwargs):
        # if request.user.is_authenticated == True and bool(request.path_info == '/accounts/login/'):
        #     print('user is deddoh')
        #     return redirect('/st-dashboard/')
        # context = self.get_context_data(**kwargs)
        # # deny permission if user is not a bursary applicant 
        # # raise PermissionDenied
        # print('error retrieving user')
        # return self.render_to_response(context)
        # ################################### not working #################
        try:
            current_user = request.user
            if current_user.is_bursarycommitteeadmin == False and current_user.is_authenticated() and (bool(request.path_info == '/') or bool(request.path_info == '/accounts/login/')):
                print('hey!')
                return redirect('/st-dashboard/')
            context = self.get_context_data(**kwargs)
            print('No Heyyy!')
            return self.render_to_response(context)

        except:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

def trial_form(request):
    return render(request, '../templates/bursary_application_form.html')

def TrialVie(request):
    
    if request.method == 'POST':
        form = TrialApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.institution = request.POST['institution']
            entry.reg = request.POST['reg']
            # entry.chief = request.POST['chief']
            form.save()
            print("saved")
        else:
            form = TrialApplicationForm()
            print("error submitting form")
    return render(request, 'home.html', locals())

class TrialView(CreateView):
    model = TrialModel
    form_class = TrialApplicationForm
    template_name = '../templates/bursary_application_form.html'

    #Redirect to this page in order to review the form data before submission 
    def form_valid(self, form):
        print('redirected to another page')
        return render(self.request, '../templates/applicant_registration.html', self.get_context_data())

    def form_invalid(self, form):

        return JsonResponse({"status": "false", "message": form.errors})
    
    
    
    # def form_valid(request, self, form):
    #     post = form.save(commit=False)
    #     post.save()
    #     print("success")
    #     return redirect('/accounts/registert')




        # return redirect('../templates/home.html')    
        # if request.method == 'POST':
        #     form = TrialApplicationForm(request.POST, request.FILE)
        #     # if form.is_valid()://////
        #     institution = form.cleaned_data.get('institution')
        #     reg = form.cleaned_data.get('reg')
        #     chief = form.cleaned_data.get('chief')
        #     form.save()
        # else:
        #     form = TrialApplicationForm()
        # return render(request, 'home.html', {'form':form})

#save reviewed bursary application form data
def bursary_form_application(request):
    if request.method == 'POST':
        form = TrialApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            school = form.cleaned_data.get('institution')
            adm = form.cleaned_data.get('reg')

            print(adm)
            
            db_schools = TrialModel.objects.all().filter(institution=school).exists()
            db_adms = TrialModel.objects.all().filter(reg=adm).exists()
            print("Reg exists: ", db_adms)

            # restrict applications to only one instance per school
            # if db_schools:
            if db_adms:
                messages.warning(request, "An application with that Registration Number already exists! Only one application  instance is allowed!")
                
            # return HttpResponseRedirect('../../st-dashboard')
            # show this error message
                return JsonResponse({"status": "Application Failed!", "message": "An application with that Registration Number already exists! Only one application  instance is allowed!"})
            else: 

                post = form.save(commit=False)
                post.user = request.user
                myDict = (request.POST).dict()
                df = pd.DataFrame(myDict, index=[0])
                # ml response
                answer = approve_reject(ohevalue(df))
                print(ohevalue(df))
                # print(df)
                # res = messages.success(request, 'Recommendation: {}'.format(answer))


                # save the ml response to database, in the Model_Recommendation field
                post.Model_Recommendation = answer

                # record exists exception
                # duplicate = TrialModel.objects.filter(user = request)

            
                # save the form to the database
                post.save()

                # redirect to the 
                return HttpResponseRedirect('../../st-dashboard')
                # return JsonResponse({"status": "success", "message": "Success"})

    

@csrf_exempt
def login_request(request):

    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                # if credentials match an applicant, redirect to student dashboard
                if user.is_bursaryapplicant == True :
                    print(user)
                    return redirect('/st-dashboard')
                # if credentials match a bursary staff member, redirect to bursary admin dashboard
                if user.is_bursarycommitteeadmin == True or user.is_superuser == True:
                    return redirect('/bc-admin')
                
            else:
                messages.error(request,"Invalid USERNAME or PASSWORD")
        else:
                messages.error(request,"Invalid USERNAME or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

# when you  log out, be redirected to the login page
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


class SubmittedApplicationsViewSet(viewsets.ModelViewSet):
    queryset = NewApplicationModel.objects.all()
    serializer_class = serializers.NewApplicationSerializer

    def perform_create(self, serializer):
        serializers.save(user=self.request.user)



##################################################################################################################################
# @login_required
@csrf_exempt
def new_application_submission(request):
    if request.method == 'POST':
        form = NewApplicationForm(request.POST or None)

        if form.is_valid():
            bursary = form.save(commit=False)
            bursary.user = request.user
            bursary.save()
                # return redirect('/accounts/login/')
            return JsonResponse({"status": "success", "message": "Success"})
            
            # return HttpResponseRedirect('/bc-admin/')
        else:
            form = NewApplicationForm()
            c = {'form': form}
        # c.update(csrf(request))
    return render(request, '../templates/home.html', c)
    #######################################################################################################################################

      
        # data = NewApplicationModel.objects.all()
        # sr = NewApplicationSerializer(data = request.POST)
        
        # if sr.is_valid():
        #     family_type = request.POST.get('family_type')
        #     guardian_for_orphan = request.POST.get('guardian_for_orphan')
        #     wishers_for_orphan = request.POST.get('wishers_for_orphan')
        #     other_for_orphan = request.POST.get('other_for_orphan')
        #     other_orphan_text = request.POST.get('other_orphan_text')
        #     fund_beneficiary_before = request.POST.get('fund_beneficiary_before')
        #     fund_amount = request.POST.get('fund_amount')
        #     fund_source = request.POST.get('fund_source')
        #     p_first_name = request.POST.get('p_first_name')
        #     p_middle_name = request.POST.get('p_middle_name')
        #     p_last_name = request.POST.get('p_last_name')
        #     p_employed = request.POST.get('p_employed')
        #     p_education = request.POST.get('p_education')
        #     p_occupation = request.POST.get('p_occupation')
        #     p_phone = request.POST.get('p_phone')
        #     p_nhif = request.POST.get('p_nhif')
        #     p_id = request.POST.get('p_id')
        #     p_pension_income = request.POST.get('p_pension_income')
        #     p_relief_income = request.POST.get('p_relief_income')
        #     p_business_income = request.POST.get('p_business_income')
        #     p_farming_income = request.POST.get('p_farming_income')
        #     p_private_groups_income = request.POST.get('p_private_groups_income')
        #     p_well_wishers_income = request.POST.get('p_well_wishers_income')
        #     p_casual_labour_income = request.POST.get('p_casual_labour_income')
        #     p_other_income = request.POST.get('p_other_income')

        #     # school details
        #     last_name = request.POST.get('last_name')
        #     first_name = request.POST.get('first_name')
        #     middle_name = request.POST.get('middle_name')
        #     value = request.POST.get('value')
        #     dob = request.POST.get('dob')
        #     name = request.POST.get('name')
        #     institution = request.POST.get('institution')
        #     course = request.POST.get('course')
        #     university_reg_no = request.POST.get('university_reg_no')
        #     university_year = request.POST.get('university_year')
        #     total_university_fee = request.POST.get('total_university_fee')
        #     paid_university_fee = request.POST.get('paid_university_fee')
        #     outstanding_university_fee = request.POST.get('outstanding_university_fee')
        #     secondary_school_name = request.POST.get('secondary_school_name')
        #     school_type = request.POST.get('school_type')
        #     total_sec_fee = request.POST.get('total_sec_fee')
        #     paid_sec_fee = request.POST.get('paid_sec_fee')
        #     outstanding_sec_fee = request.POST.get('outstanding_sec_fee')
        #     class_name = request.POST.get('class_name')
        #     sec_reg_no = request.POST.get('sec_reg_no')
        #     sec_year = request.POST.get('sec_year')
        #     school = request.POST.get('school')

        #     # location    
        #     sub_county = request.POST.get('sub_county')
        #     ward = request.POST.get('ward')
        #     village = request.POST.get('village')
        #     year = request.POST.get('year')

        #     sr.save()
        #     return JsonResponse(sr.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(sr.errors, status=status.HTTP_400_BAD_REQUEST)
          
            # data = form.cleaned_data
            # new_application_model = NewApplicationModel.objects.create(**data, user=request.user)






# get all submitted bursary applications
def get_applications(request):
    data = SubmittedApplicationsModel.objects.all()
    if request.method == 'GET':
        # first_name = BursaryApplicant.objects.get(first_name='first_name', flat=True)
        
        serializer = SubmittedApplicationsModelSerializer(data, many=True)

        return JsonResponse( serializer.data, safe=False)

# get all registered applicants in the Admin view
def registered_applicants(request):
    data = BursaryApplicant.objects.all()

    if request.method == 'GET':
        serializer = BursaryApplicantSerializer(data, many=True)
        # print(data)
        return JsonResponse(serializer.data, safe=False)

#  trials 
def show_submissions(request):
    # data = TrialModel.objects.filter(first_name__first_name  )
    # data = TrialModel.objects.filter(fname__first_name = request.user)
    ffname = TrialModel.objects.all()
    # data = TrialModel.objects.filter(id=29).values('id','fname.first_name', 'fname__first_name', 'fname__last_name', 'institution',
    #         'reg', 'year_of_study', 'total_fee', 'paid', 'outstanding_balance', 'fund_source', 'fund_source_amount',
    #         'pension_income', 'relief_income', 'business_income', 'farming_income', 
    #         'private_groups_income', 'well_wishers_income', 'casual_labour_income', 'other_income',  'guardian_as_financier', 
    #         'well_wishers_as_financier', 'other_financier', 'other_financiers', 'p_first_name','p_middle_name','p_last_name', 
    #         'p_occupation', 'p_phone', 'p_id_number', 'p_employed', 'p_education_level', 'p_nhif', 'father_gross_income', 
    #         'guardian_gross_income', 'mother_gross_income','number_of_siblings', 'guardian_children', 'working_siblings', 
    #         'siblings_in_secondary', 'siblings_in_post_secondary', 'school_rep_name', 
    #         'school_document', 'chief_name', 'chief_document', 'mca_name', 'mca_document', 'clergy_name', 
    #         'clergy_document', 'transcript_document', 'fee_structure_document', 'fee_slip_document' )

    # data = TrialModel.objects.filter(user_id=29).values( 'user_id', 'user_id__first_name', 'user_id__last_name')

    # data = TrialModel.objects.filter(fname__user=request.user)
    data = TrialModel.objects.all()

    if request.method == 'GET':
        serializer = TrialModelSerializer(data, many=True)
        # print(data)
        return JsonResponse(serializer.data, safe=False)

def loggedUser(request):
    # username = None
    data = BursaryApplicant.objects.filter(user=request.user)

    if request.method == 'GET':
        serializer = BursaryApplicantSerializer(data, many=True)
            # if request.user.is_authenticated():
        first_name = request.user.first_name
        email = request.user.email
        print(first_name)
        print(email)
        return JsonResponse( serializer.data, safe=False)

def awardedApplicant(request):
    # username = None
    data = TrialModel.objects.filter(user=request.user)

    if request.method == 'GET':
        serializer = TrialModelSerializer(data, many=True)
            # if request.user.is_authenticated():
        first_name = request.user.first_name
        email = request.user.email
        print(first_name)
        print(email)
        return JsonResponse( serializer.data, safe=False)

def apply(request):
    data = NewBursaryApplication.objects.all()
    

def check_login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'result': {'logged': True}, 'user': request.user.username}),
        content_type="application/json")
    else: return HttpResponse(json.dumps({'result': {'logged': False}}),
    content_type="application/json")

# CRUD OPERATIONS

# DELETE
@csrf_exempt
def deleteapplicant(request, id):
    if request.method == 'DELETE':
        TrialModel.objects.filter(id=id).delete()
        return JsonResponse({"status": "success", "message": "Item deleted successfully!"})


# UPDATE

# @csrf_exempt
# @api_view(['PUT'])
# def update_application_status(request, id):
#     task = TrialModel.objects.get(id=id)
#     serializer = TrialModelSerializer(instance = task, data=request.POST)
#     if serializer.is_valid():
#         print("serializer", serializer)
#         print("serializer.data", serializer.data)
#         serializer.save()

#         return JsonResponse(serializer.data)
#     return JsonResponse(serializer.errors)

# @csrf_exempt
# def update_application_status(instance, *args, **kwargs):
#     instance.institution = validated_data.get('institution', instance.institution)
#     instance.reg = validated_data.get('reg', instance.reg)
#     print(instance)
#     instance.save()
#     return instance

# @csrf_exempt
@api_view(['PUT'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def update_application_status(request, id):
    instance = TrialModel.objects.get(id=id)

    # use request.data.get instead of request.POST to get data from external api
    instance.institution = request.data.get('institution', instance.institution)
    instance.reg = request.data.get('reg', instance.reg)
    instance.year_of_study = request.data.get('year_of_study', instance.year_of_study)
    instance.total_fee = request.data.get('total_fee', instance.total_fee)
    instance.paid = request.data.get('paid', instance.paid)
    instance.outstanding_balance = request.data.get('outstanding_balance', instance.outstanding_balance)
    instance.Bursary_Application_Status = request.data.get('Bursary_Application_Status', instance.Bursary_Application_Status)
    instance.amount_allocated = request.data.get('amount_allocated', instance.amount_allocated)
    instance.description = request.data.get('description', instance.description)

    print(request.POST.get('institution', instance.institution))
    instance.save(update_fields=['institution'])
    

    serializer = TrialModelSerializer(instance=instance, data=request.POST)
    if serializer.is_valid():
       
        
        serializer.save()
       
        return Response(serializer.data)


# Reports data
# approved applications
def all_approved_applications(request):
    data = TrialModel.objects.all().filter(Bursary_Application_Status="APPROVED")
    if request.method == "GET":
        
        serializer = TrialModelSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

#rejected applications
def all_rejected_applications(request):
    data = TrialModel.objects.all().filter(Bursary_Application_Status="UNSUCCESSFUL")
    if request.method == "GET":
        
        serializer = TrialModelSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

# under review
def under_review_applications(request):
    data = TrialModel.objects.all().filter(Bursary_Application_Status="REVIEW_IN_PROCESS")
    if request.method == "GET":
        
        serializer = TrialModelSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)