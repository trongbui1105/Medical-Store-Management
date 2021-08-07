from rest_framework import serializers
from .models import *

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

class MedicineSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = CompanySerialiazer(instance.company_id).data
        return response

class MedicalDetailsSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDetails
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['medicine'] = MedicineSerialiazer(instance.medicine_id).data
        return response

class MedicalDetailsSerialiazerSimple(serializers.ModelSerializer):
    class Meta:
        model = MedicalDetails
        fields = '__all__'
        

class EmployeeSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CustomerSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class BillSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerialiazer(instance.customer_id).data
        return response

class CustomerRequestSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequest
        fields = '__all__'

class CompanyAccountSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAccount
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = CompanySerialiazer(instance.company_id).data
        return response

class EmployeeBankSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBank
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = EmployeeSerialiazer(instance.employee_id).data
        return response

class EmployeeSalarySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = EmployeeSerialiazer(instance.employee_id).data
        return response