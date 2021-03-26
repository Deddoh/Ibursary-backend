from django.contrib.auth.forms import UserCreationForm
# send details to the db as soon as its submitted, in a single transaction
from django.db import transaction
from django import forms
from django.forms import ModelForm
from .models import User, BursaryCommitteeAdmin, BursaryApplicant, NewApplicationModel, TrialModel
KIAMBU_SUB_COUNTIES= [
    ('', '--select sub county --'),
    ('Thika Town', 'Thika Town'),
    ('Gatundu North', 'Gatundu North'),
    ('Gatundu South', 'Gatundu South'),
    ('Juja', 'Juja'),
    ('Lari', 'Lari'),
    ('Kikuyu', 'Kikuyu'),
    ('Githunguri', 'Githunguri'),
    ('Kabete', 'Kabete'),
    ('Ruiru', 'Ruiru'),
    ('Limuru', 'Limuru'),
    ('Kiambaa', 'Kiambaa'),
    ('Kiambu', 'Kiambu')
 ]

KIAMBU_WARDS = [
    ('', '--select ward--'),
    ('Township Ward', 'Township Ward'),
    ('Kamenu Ward', 'Kamenu Ward'),
    ('Hospital Ward', 'Hospital Ward'),
    ('Gatuanyaga Ward', 'Gatuanyaga Ward'),
    ('Gituamba Ward', 'Gituamba Ward'),
    ('Githobokoni Ward', 'Githobokoni Ward'),
    ('Chania Ward', 'Chania Ward'),
    ("Mang'u Ward", "Mang'u Ward"),
    ('Kiamwangi Ward', 'Kiamwangi Ward'),
    ('Kiganjo Ward', 'Kiganjo Ward'),
    ('Ndarugo Ward', 'Ndarugo Ward'),
    ('Ngendo Ward', 'Ngendo Ward'),
    ('Murera Ward', 'Murera Ward'),
    ('Theta Ward', 'Theta Ward'),
    ('Witeithia Ward', 'Witeithie'),
    ('Kalimoni Ward', 'Kalimoni Ward'),
    ('Kinale Ward', 'Kinale Ward'),
    ('Kijabe Ward', 'Kijabe Ward'),
    ('Nyanduma Ward', 'Nyanduma Ward'),
    ('Kamburu Ward', 'Kamburu Ward'),
    ('Lari/Kirenga Ward', 'Lari/Kirenga Ward'),
    ('Karai Ward', 'Karai Ward'),
    ('Nachu Ward', 'Nachu Ward'),
    ('Sigona Ward', 'Sigona Ward'),
    ('Kikuyu Ward', 'Kikuyu Ward'),
    ('Kinoo Ward', 'Kinoo Ward'),
    ('Githunguri Ward', 'Githunguri Ward'),
    ('Githiga Ward', 'Githiga Ward'),
    ('Ikinu Ward', 'Ikinu Ward'),
    ('Ngewa Ward', 'Ngewa Ward'),
    ('Komothai 3 Ward', 'Komothai 3 Ward'),
    ('Gitaru Ward', 'Gitaru Ward'),
    ('Muguga Ward', 'Muguga ward'),
    ('Nyadhuna Ward', 'Nyadhuna Ward'),
    ('Kabete Ward', 'Kabete Ward'),
    ('Uthiru Ward', 'Uthiru Ward'),
    ('Gitothua Ward', 'Gitothua Ward'),
    ('Biashara Ward', 'Biashara Ward'),
    ('Gatongora Ward', 'Gatongora Ward'),
    ('Kahawa /Sukari Ward', 'Kahawa/Sukari Ward'),
    ('Kahawa Wendani', 'Kahawa Wendani'),
    ('Kiuu Ward Mwiki Ward', 'Kiuu Ward Mwiki Ward'),
    ('Mwihoko 1 Ward', 'Mwihoko 1 Ward'),
    ('Bibirioni Ward', 'Bibirioni Ward'),
    ('Limuru Central Ward', 'Limuru Central Ward'),
    ('Ndeiya Ward', 'Ndeiya Ward'),
    ('Limuru East Ward', 'Limuru East Ward'),
    ('Ngecha Tigoni Ward', 'Ngecha Tigoni Ward'),
    ('Cianda Ward', 'Cianda Ward'),
    ('Karuri Ward', 'Karuri Ward'),
    ('Ndenderu Ward', 'Ndenderu Ward'),
    ('Muchatha Ward', 'Muchatha Ward'),
    ('Kihara Ward', 'Kihara Ward'),
    ("Ting'ang'a Ward", "Ting'ang'a Ward"),
    ('Ndumberi 3 Ward', 'Ndumberi 3 Ward'),
    ('Riabai Ward', 'Riabai Ward'),
    ('Township Ward', 'Township Ward')
]

GENDER = [
    ('Male', 'Male'),
    ('Female','Female')
]

Parental_Status = [
    ('both_parents_alive', 'Both Parents Alive'),
    ('total_orphan', 'Orphan: Both biological parents deceased'),
    ('partial_orphan', 'Abandoned')
]


# student registration form
class ApplicantSignUpForm(UserCreationForm):
    # applicant_full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Please enter full name'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Please enter first name'}))
    middle_name = forms.CharField(required=True, widget= forms.TextInput(attrs={'placeholder': 'Enter middle name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    # id_number = forms.IntegerField(required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter phone number'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'required': 'required'}))
    county = forms.CharField(max_length=100, initial="Kiambu", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    sub_county = forms.CharField(max_length = 100, widget=forms.Select(choices=KIAMBU_SUB_COUNTIES, attrs={'placeholder': ('--select sub-county--')}))
    ward = forms.CharField(max_length = 20, widget=forms.Select(choices=KIAMBU_WARDS, attrs={'placeholder': ('--select ward--')}))
    sub_location = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'placeholder': 'Enter sub-location'}))
    
    


    # def __init__(self, *args, **kwargs):
    #     super(ApplicantSignUpForm, self).__init__(*args, **kwargs)
    #     self.fields['sub_county'].widget = forms.Select(attrs={'placeholder':('--select sub county--')})


 

    class Meta(UserCreationForm.Meta):
        model = User

    
    # save changes in db if the code block is successfully run
    @transaction.atomic
    # function to save to db
    def save(self):
        user = super().save(commit=False)
        user.is_bursaryapplicant = True
        # user.applicant_full_name = self.cleaned_data.get('applicant_full_name')
        user.first_name = self.cleaned_data.get('first_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.ward = self.cleaned_data.get('ward')
        user.save()
        applicant = BursaryApplicant.objects.create(user=user)
        # applicant.applicant_full_name = self.cleaned_data.get('applicant_full_name')
        applicant.first_name = self.cleaned_data.get('first_name')
        applicant.middle_name = self.cleaned_data.get('middle_name')
        applicant.last_name = self.cleaned_data.get('last_name')
        # applicant.ID_number = self.cleaned_data.get('id_number')
        applicant.Email = self.cleaned_data.get('email')
        applicant.Phone_number = self.cleaned_data.get('phone')
        applicant.Date_of_birth = self.cleaned_data.get('date_of_birth')
        applicant.County = self.cleaned_data.get('county')
        applicant.Sub_County = self.cleaned_data.get('sub_county')
        applicant.Ward = self.cleaned_data.get('ward')
        applicant.Sub_location = self.cleaned_data.get('sub_location')
        
        applicant.save()

        # trialmodel names
        # submission = TrialModel.objects.create(user=user)
        # submission.first_name = self.cleaned_data.get('first_name')
        # submission.middle_name = self.cleaned_data.get('middle_name')
        # submission.last_name = self.cleaned_data.get('last_name')
        # submission.save()
        return user


# committee admin sign up form
class BursaryAdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    ID_Number = forms.CharField(required=True)
    phone = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_bursarycommitteeadmin = True
        user.first_name = self.cleaned_data.get('first_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        b_admin = BursaryCommitteeAdmin.objects.create(user=user)
        b_admin.ID_number = self.cleaned_data.get('ID_Number')
        b_admin.phone_number = self.cleaned_data.get('phone')
        b_admin.save()
        return user



class NewApplicationForm(forms.ModelForm):

    class Meta:
        model = NewApplicationModel
        # fields = ['family_type', 'guardian_for_orphan', 'wishers_for_orphan', 'other_for_orphan', 'other_orphan_text', 'fund_beneficiary_before', 'fund_amount', 'fund_source', 'p_first_name', 'p_middle_name', 'p_last_name', 'p_employed', 'p_education', 'p_occupation', 'p_phone', 'p_nhif', 'p_id', 'p_pension_income', 'p_business_income', 'p_farming_income', 'p_private_groups_income', 'p_well_wishers_income', 'p_casual_labour_income', 'p_other_income', 'last_name', 'first_name', 'middle_name', 'value', 'dob', 'name', 'institution', 'course', 'university_reg_no', 'university_year', 'total_university_fee', 'paid_university_fee', 'outstanding_university_fee', 'secondary_school_name', 'school_type', 'total_sec_fee', 'paid_sec_fee', 'outstanding_sec_fee', 'class_name', 'sec_reg_no', 'sec_year', 'school', 'sub_county', 'ward', 'village', 'year' ]
        fields = ['p_first_name']

class TrialApplicationForm(forms.ModelForm):


    class Meta:
        model = TrialModel
        fields = [
            'school_type', 'status','disability','disability_form', 'benefitted','user','gender', 'phone_number',
            'institution', 'reg', 'year_of_study', 'total_fee', 'paid', 'outstanding_balance', 'fund_source', 'fund_source_amount',
            'pension_income', 'relief_income', 'business_income', 'farming_income', 
            'private_groups_income', 'well_wishers_income', 'casual_labour_income', 'other_income',  'p_first_name','p_middle_name','p_last_name', 
            'p_occupation', 'p_phone', 'p_id_number', 'p_employed', 'p_education_level', 'p_nhif', 'father_gross_income', 
            'guardian_gross_income', 'mother_gross_income','number_of_siblings', 'guardian_children', 'working_siblings', 
            'siblings_in_secondary', 'siblings_in_post_secondary', 'school_rep_name', 
            'school_document', 'chief_name', 'chief_document', 'mca_name', 'mca_document', 'clergy_name', 
            'clergy_document', 'transcript_document', 'fee_structure_document', 'fee_slip_document', 
            'student_declaration', 'parent_guardian_declaration'
            ]

        widgets = {

            # 'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required':'required'}),
            # 'middle_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required':'required'}),
            # 'last_name' : forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required':'required'}),
            'institution': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required'}),
            'reg': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'gender' : forms.Select(choices=GENDER,attrs={'class': 'form-control form-control-lg'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'year_of_study': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'total_fee': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'paid': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'outstanding_balance': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'fund_source': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'fund_source_amount': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'pension_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'relief_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'business_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'farming_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'private_groups_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'well_wishers_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'casual_labour_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'other_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'chief': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),

            # 'guardian_as_financier': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id':'gaf', 'name':'gaf'}),
            # 'well_wishers_as_financier': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id':'waf', 'name':'waf'}),
            # 'other_financier': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'other_financiers': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),

            'p_first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_middle_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_occupation': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_phone': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'disability': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'disability_form': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Please enter your form of disability'}),
            'status': forms.Select(choices=Parental_Status, attrs={'class': 'form-control form-control-lg'}),
            'school_type': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'benefitted': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_id_number': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_employed': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_education_level': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'p_nhif': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'father_gross_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'guardian_gross_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'mother_gross_income': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'number_of_siblings': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'guardian_children': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'working_siblings': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'siblings_in_secondary': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'siblings_in_post_secondary': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'sibling_f_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'sibling_school': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'sibling_class': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'sibling_total_fee': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'sibling_fee_paid': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'sibling_balance': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'second_sibling_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'second_sibling_school': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'second_sibling_class': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'second_sibling_total_fee': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'second_sibling_fee_paid': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'second_sibling_balance': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'third_sibling_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'third_sibling_school': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'third_sibling_class': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'third_sibling_total_fee': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'third_sibling_fee_paid': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'third_sibling_balance': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'fourth_sibling_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'fourth_sibling_school': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'fourth_sibling_class': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'fourth_sibling_total_fee': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'fourth_sibling_fee_paid': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            # 'fourth_sibling_balance': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'school_rep_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'school_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'chief_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'chief_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'mca_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'mca_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'clergy_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'clergy_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'transcript_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'fee_structure_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'fee_slip_document': forms.FileInput(attrs={'accept': '.pdf, .doc', 'class': 'file'}),
            'student_declaration': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'parent_guardian_declaration': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            

        }
