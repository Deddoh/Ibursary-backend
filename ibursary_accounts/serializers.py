from rest_framework import serializers
from .models import SubmittedApplicationsModel, BursaryApplicant, NewApplicationModel, TrialModel
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class SubmittedApplicationsModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = SubmittedApplicationsModel
        fields= '__all__'

class BursaryApplicantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BursaryApplicant
        fields = '__all__'

class NewApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = NewApplicationModel
        fields = '__all__'

class TrialModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    # first_name = serializers.StringRelatedField(many=False)
    class Meta:
        model = TrialModel
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance.institution = validated_data.get('institution', instance.institution)
    #     instance.save()
    #     return instance