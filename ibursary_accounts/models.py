from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    is_bursaryapplicant = models.BooleanField(default=False)
    is_bursarycommitteeadmin = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    ward = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)

    # def __str__(self):

    #     return self.name
        
        

class BursaryApplicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name= models.CharField(max_length=200)
    # applicant_full_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    ID_number = models.CharField(max_length = 10)
    Email = models.EmailField()
    phone_regex = RegexValidator(
		regex=r'^\+?1?\d{9,15}$',
		message="Phone number must be entered in the format: '+254700000000'. Up to 15 digits allowed.")
    Phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list
    Date_of_birth = models.CharField(max_length = 20)
    County = models.CharField(max_length=100, default="Kiambu")
    Sub_County = models.CharField(max_length = 100, default='Ruiru')
    Ward = models.CharField(max_length = 20, default='Kahawa Wendani')
    Sub_location = models.CharField(max_length=100, null=True )
    

    # def clean(self):
    #     self.first_name = name

#####################################

    # def __str__(self):
    #     return str(self.applicant_full_name)
    # def __str__(self):
    #     return '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)

    def __str__(self):
        return self.Ward
    
#####################################

class NewApplicationModel(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_bursaryapplicant': True})
    user = models.ForeignKey(BursaryApplicant, on_delete=models.CASCADE , related_name='bursary_applicant')
    family_type = models.CharField(max_length=100, null=True)
    guardian_for_orphan = models.CharField(max_length=100, null=True)
    wishers_for_orphan = models.CharField(max_length=100, null=True)
    other_for_orphan = models.CharField(max_length=100, null=True)
    other_orphan_text = models.CharField(max_length=100, null=True)
    fund_beneficiary_before = models.CharField(max_length=100, null=True)
    fund_amount = models.CharField(max_length=100, null=True)
    fund_source = models.CharField(max_length=100, null=True)
    p_first_name = models.CharField(max_length=100, null=True)
    p_middle_name = models.CharField(max_length=100, null=True)
    p_last_name = models.CharField(max_length=100, null=True)
    p_employed = models.CharField(max_length=100, null=True)
    p_education = models.CharField(max_length=100, null=True)
    p_occupation = models.CharField(max_length=100, null=True)
    p_phone = models.CharField(max_length=100, null=True)
    p_nhif = models.CharField(max_length=100, null=True)
    p_id = models.CharField(max_length=100, null=True)
    p_pension_income = models.CharField(max_length=100, null=True)
    p_relief_income = models.CharField(max_length=100, null=True)
    p_business_income = models.CharField(max_length=100, null=True)
    p_farming_income = models.CharField(max_length=100, null=True)
    p_private_groups_income = models.CharField(max_length=100, null=True)
    p_well_wishers_income = models.CharField(max_length=100, null=True)
    p_casual_labour_income = models.CharField(max_length=100, null=True)
    p_other_income = models.CharField(max_length=100, null=True)

    # school details
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, null=True)
    course = models.CharField(max_length=100, null=True)
    university_reg_no = models.CharField(max_length=100, null=True)
    university_year = models.CharField(max_length=100, null=True)
    total_university_fee = models.CharField(max_length=100, null=True)
    paid_university_fee = models.CharField(max_length=100, null=True)
    outstanding_university_fee = models.CharField(max_length=100, null=True)
    secondary_school_name = models.CharField(max_length=100, null=True)
    school_type = models.CharField(max_length=100, null=True)
    total_sec_fee = models.CharField(max_length=100, null=True)
    paid_sec_fee = models.CharField(max_length=100, null=True)
    outstanding_sec_fee = models.CharField(max_length=100, null=True)
    class_name = models.CharField(max_length=100, null=True)
    sec_reg_no = models.CharField(max_length=100, null=True)
    sec_year = models.CharField(max_length=100, null=True)
    school = models.CharField(max_length=100, null=True)

    # location    
    sub_county = models.CharField(max_length=100, null=True)
    ward = models.CharField(max_length=100, null=True)
    village = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)

    
    

class BursaryCommitteeAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ID_number = models.IntegerField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+254700000000'. Up to 15 digits allowed. "
    )
    phone_number = models.CharField(validators=[phone_regex], blank=False, max_length=17)


# view all submitted applications
class SubmittedApplicationsModel(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_bursaryapplicant': True})
    institution = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    voter = models.CharField(max_length=100)
    creation_date = models.CharField(max_length=100)

    

    # def clean(self):
    #     self.user = name

    def __str__(self):
        return self.name


    # def save(self, *args, **kwargs):
    #     if self.id_number:
    #         self.creation_date = timezone.now()
    #     return super(User, self).save(*args, **kwargs)


class TrialModel(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_bursaryapplicant': True},null=True, blank=True)
    # first_name = models.CharField(max_length=100, null=True)
    # first_name = models.ForeignKey(BursaryApplicant, on_delete=models.CASCADE, null=True, blank=True)
    
    # first_name = models.ForeignKey(BursaryApplicant, on_delete=models.CASCADE, null=True, blank=True)
    Model_Recommendation = models.CharField(max_length=40, null=True, blank=True)
    Bursary_Application_Status = models.CharField(default='REVIEW_IN_PROCESS', max_length=100)
    amount_allocated = models.CharField(default="0", max_length=5)
    description = models.CharField(max_length=200, null=True, blank=True)
    # middle_name = models.CharField(max_length=100, null=True)
    # last_name = models.CharField(max_length=100, null=True)
    ward = models.ForeignKey(BursaryApplicant, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    disability = models.CharField(max_length=3, null=True, blank=True)
    disability_form = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # fname = models.ForeignKey('BursaryApplicant',related_name="bursaryapplicant", null=True, on_delete = models.CASCADE)
    school_type = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    school_admitted = models.CharField(max_length=100, null=True, blank=True)
    reg = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.CharField(max_length=100, null=True)
    total_fee =  models.CharField(max_length=100, null=True)
    paid = models.CharField(max_length=100, null=True)
    outstanding_balance = models.CharField(max_length=100, null=True)
    disability = models.CharField(max_length=3, null=True)
    disability_form = models.CharField(max_length=20, null=True, blank=True)

    # parent's details

    fund_source = models.CharField(max_length=100, null=True, blank=True)
    fund_source_amount = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True)
    benefitted = models.CharField(max_length=100, null=True)

    pension_income = models.CharField(max_length=100, null=True)
    relief_income = models.CharField(max_length=100, null=True)
    business_income = models.CharField(max_length=100, null=True)
    farming_income = models.CharField(max_length=100, null=True)
    private_groups_income =models.CharField(max_length=100, null=True)
    well_wishers_income = models.CharField(max_length=100, null=True)
    casual_labour_income = models.CharField(max_length=100, null=True)
    other_income = models.CharField(max_length=100, null=True)

    # guardian_as_financier = models.BooleanField( default=False)
    # well_wishers_as_financier = models.BooleanField(default=False)
    # other_financier = models.BooleanField(default=False)
    # other_financiers = models.CharField(max_length=100, null=True, blank=True)

    p_first_name = models.CharField(max_length=100, null=True)
    p_middle_name = models.CharField(max_length=100, null=True)
    p_last_name = models.CharField(max_length=100, null=True)
    p_occupation = models.CharField(max_length=100, null=True)
    p_phone = models.CharField(max_length=100, null=True)
    p_id_number = models.CharField(max_length=100, null=True)
    p_employed = models.CharField(max_length=100, null=True)
    p_education_level = models.CharField(max_length=100, null=True)
    p_nhif = models.CharField(max_length=100, null=True, blank=True)

    father_gross_income = models.CharField(max_length=100, null=True)
    mother_gross_income = models.CharField(max_length=100, null=True)
    guardian_gross_income = models.CharField(max_length=100, null=True)

    number_of_siblings = models.CharField(max_length=100, null=True)
    guardian_children = models.CharField(max_length=100, null=True, blank=True)
    working_siblings = models.CharField(max_length=100, null=True)
    siblings_in_secondary = models.CharField(max_length=100, null=True)
    siblings_in_post_secondary = models.CharField(max_length=100, null=True)

    # sibling_f_name = models.CharField(max_length=100, null=True, blank=True)
    # sibling_school = models.CharField(max_length=100, null=True, blank=True)
    # sibling_class = models.CharField(max_length=100, null=True, blank=True)
    # sibling_total_fee = models.CharField(max_length=100, null=True, blank=True)
    # sibling_fee_paid = models.CharField(max_length=100, null=True, blank=True)
    # sibling_balance = models.CharField(max_length=100, null=True, blank=True)

    # second_sibling_name = models.CharField(max_length=100, null=True, blank=True)
    # second_sibling_school = models.CharField(max_length=100, null=True, blank=True)
    # second_sibling_class = models.CharField(max_length=100, null=True, blank=True)
    # second_sibling_total_fee = models.CharField(max_length=100, null=True, blank=True)
    # second_sibling_fee_paid = models.CharField(max_length=100, null=True, blank=True)
    # second_sibling_balance = models.CharField(max_length=100, null=True, blank=True)

    # third_sibling_name = models.CharField(max_length=100, null=True, blank=True)
    # third_sibling_school = models.CharField(max_length=100, null=True, blank=True)
    # third_sibling_class = models.CharField(max_length=100, null=True, blank=True)
    # third_sibling_total_fee = models.CharField(max_length=100, null=True, blank=True)
    # third_sibling_fee_paid = models.CharField(max_length=100, null=True, blank=True)
    # third_sibling_balance = models.CharField(max_length=100, null=True, blank=True)

    # fourth_sibling_name = models.CharField(max_length=100, null=True, blank=True)
    # fourth_sibling_school = models.CharField(max_length=100, null=True, blank=True)
    # fourth_sibling_class = models.CharField(max_length=100, null=True, blank=True)
    # fourth_sibling_total_fee = models.CharField(max_length=100, null=True, blank=True)
    # fourth_sibling_fee_paid = models.CharField(max_length=100, null=True, blank=True)
    # fourth_sibling_balance = models.CharField(max_length=100, null=True, blank=True)  

    # docs source
    school_rep_name = models.CharField(max_length=100, null=True) 
    chief_name = models.CharField(max_length=100, null=True) 
    clergy_name = models.CharField(max_length=100, null=True) 
    mca_name = models.CharField(max_length=100, null=True) 

    # declarations
    student_declaration = models.CharField(max_length=100, null=True) 
    parent_guardian_declaration = models.CharField(max_length=100, null=True) 

    # documents
    school_document = models.FileField(upload_to="school_docs/", default="fi")
    chief_document = models.FileField(upload_to="chief_docs/", default="fi")
    mca_document = models.FileField(upload_to="mca_docs/", default="fi")
    clergy_document = models.FileField(upload_to="religious_leader_docs/", default="fi")
    transcript_document = models.FileField(upload_to="transcript_docs/", default="fi")
    fee_structure_document = models.FileField(upload_to="fee_structure_docs/", default="fi")
    fee_slip_document = models.FileField(upload_to="fee_slip_docs/", default="fi")

    created_at = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return self.first_name






