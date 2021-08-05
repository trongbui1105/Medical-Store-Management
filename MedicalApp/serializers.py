from rest_framework import serializers
from .models import Company, CompanyBank

class CompanySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBank
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = CompanySerialiazer(instance.company_id).data
        return response
