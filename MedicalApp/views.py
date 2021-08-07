from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.
class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerialiazer(company, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Data"}
        return Response(dict_response)
    
    def update(self, request, pk=None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk = pk)
            serializer = CompanySerialiazer(company, data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Data"}

        return Response(dict_response)

class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Bank Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Bank Data"}
        return Response(dict_response)

    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Company Bank List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk = None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk = pk)
        serializer = CompanyBankSerializer(companybank, context = {"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk = None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk = pk)
        serializer = CompanyBankSerializer(companybank, data = request.data, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerialiazer
    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name = name)


class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()

            medicine_id = serializer.data["id"]
            # Access the serializer ID which just save in our db table
            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                print(medicine_detail)
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerialiazer(data = medicine_details_list, many = True, context = {"request": request})
            serializer2.is_valid()
            serializer2.save()

            dict_response = {"error": False, "message": "Medicine Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Medicine Data"}
        return Response(dict_response)

    def list(self, request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerialiazer(medicine, many = True, context = {"request": request})

        medicine_data = serializer.data
        newmedicinelist = []

        # Adding extra key for Medicine Details in Medicine
        for medicine in medicine_data:
            #Access All the Medicine Details of Current Medicine ID
            medicine_details = MedicalDetails.objects.filter(medicine_id = medicine["id"])
            medicine_details_serializers = MedicalDetailsSerialiazerSimple(medicine_details, many = True)
            medicine["medicine_details"] = medicine_details_serializers.data
            newmedicinelist.append(medicine)

        response_dict = {"error": False, "message": "All Medicine List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk = None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk = pk)
        serializer = MedicineSerialiazer(medicine, context = {"request": request})

        serializer_data = serializer.data
         #Access All the Medicine Details of Current Medicine ID
        medicine_details = MedicalDetails.objects.filter(medicine_id = serializer_data["id"])
        medicine_details_serializers = MedicalDetailsSerialiazerSimple(medicine_details, many = True)
        serializer_data["medicine_details"] = medicine_details_serializers.data
        

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk = None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk = pk)
        serializer = MedicineSerialiazer(medicine, data = request.data, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})

company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})