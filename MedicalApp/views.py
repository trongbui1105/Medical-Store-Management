from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from datetime import datetime, timedelta

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

    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerialiazer(company, context={"request": request})

        serializer_data = serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        company_bank_details = CompanyBank.objects.filter(company_id = serializer_data["id"])
        companybank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        serializer_data["company_bank"] = companybank_details_serializers.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
    
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

    def delete(self, request, pk = id):
        try:
            companybank = CompanyBank.objects.filter(id=pk)
            companybank.delete()
            dict_response = {"error": False, "message": "Data Has Been Deleted"}
        except:
            dict_response = {"error": True, "message": "Error During Deleting Company Bank Data"}
        return Response(dict_response)


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerialiazer
    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name = name)

class MedicineByNameViewSet(generics.ListAPIView):
    serializer_class = MedicineSerialiazer
    def get_queryset(self):
        name = self.kwargs["name"]
        return Medicine.objects.filter(name__contains = name)

class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerialiazer
    def get_queryset(self):
        return Company.objects.all()


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
        for salt_detail in request.data["medicine_details"]:
            if salt_detail["id"] == 0:
                # For Insert New Salt Details
                del salt_detail["id"]
                salt_detail["medicine_id"] = serializer.data["id"]
                serializer2 = MedicalDetailsSerialiazer(data = salt_detail, context = {"request": request})
                serializer2.is_valid()
                serializer2.save()
            else:
                # For Update Salt Details
                queryset2 = MedicalDetails.objects.all()
                medicine_salt = get_object_or_404(queryset2, pk=salt_detail["id"])
                del salt_detail["id"]
                serializer3 = MedicalDetailsSerialiazer(medicine_salt, data = salt_detail, context = {"request": request})
                serializer3.is_valid()
                serializer3.save()
        return Response({"error": False, "message": "Data Has Been Updated"})

    def delete(self, request, pk = id):
        queryset = Medicine.objects.filter()
        medicine = get_object_or_404(queryset, pk = pk)
        medicine.delete()

        return Response({"error": False, "message": "Medicine Data Delete Successfully"})

#Company Account Viewset
class CompanyAccountViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyAccountSerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Account Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Account Data"}
        return Response(dict_response)

    def list(self, request):
        companyAccount = CompanyAccount.objects.all()
        serializer = CompanyAccountSerialiazer(companyAccount, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Company Account List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk = None):
        queryset = CompanyAccount.objects.all()
        companyAccount = get_object_or_404(queryset, pk = pk)
        serializer = CompanyAccountSerialiazer(companyAccount, context = {"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk = None):
        queryset = CompanyAccount.objects.all()
        companyAccount = get_object_or_404(queryset, pk = pk)
        serializer = CompanyAccountSerialiazer(companyAccount, data = request.data, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})


# Employee Viewset
class EmployeeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = EmployeeSerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Employee Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Employee Data"}
        return Response(dict_response)

    def list(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerialiazer(employee, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Employee List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk = None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset, pk = pk)
        serializer = EmployeeSerialiazer(employee, context = {"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk = None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset, pk = pk)
        serializer = EmployeeSerialiazer(employee, data = request.data, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})

    def delete(self, request, pk = id):
        queryset = Employee.objects.filter()
        employee = get_object_or_404(queryset, pk = pk)
        employee.delete()

        return Response({"error": False, "message": "Employee Data Delete Successfully"})

# Employee Bank Viewset
class EmployeeBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = EmployeeBankSerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Employee Bank Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Employee Bank Data"}
        return Response(dict_response)

    def list(self, request):
        employeeBank = EmployeeBank.objects.all()
        serializer = EmployeeBankSerialiazer(employeeBank, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Employee Bank List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk = None):
        queryset = EmployeeBank.objects.all()
        employeeBank = get_object_or_404(queryset, pk = pk)
        serializer = EmployeeBankSerialiazer(employeeBank, context = {"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk = None):
        queryset = EmployeeBank.objects.all()
        employeeBank = get_object_or_404(queryset, pk = pk)
        serializer = EmployeeBankSerialiazer(employeeBank, data = request.data, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})

# Employee Salary Viewset
class EmployeeSalaryViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = EmployeeSalarySerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Employee Salary Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Employee Salary Data"}
        return Response(dict_response)

    def list(self, request):
        employeeSalary = EmployeeSalary.objects.all()
        serializer = EmployeeSalarySerialiazer(employeeSalary, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Employee Salary List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk = None):
        queryset = EmployeeSalary.objects.all()
        employeeSalary = get_object_or_404(queryset, pk = pk)
        serializer = EmployeeSalarySerialiazer(employeeSalary, context = {"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk = None):
        queryset = EmployeeSalary.objects.all()
        employeeSalary = get_object_or_404(queryset, pk = pk)
        serializer = EmployeeSalarySerialiazer(employeeSalary, data = request.data, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})


class EmployeeBankByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeBankSerialiazer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        employee_id = self.kwargs["employee_id"]
        return  EmployeeBank.objects.filter(employee_id = employee_id)


class EmployeeSalaryByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeSalarySerialiazer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        employee_id = self.kwargs["employee_id"]
        return  EmployeeSalary.objects.filter(employee_id = employee_id)

class GenerateBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            #Save Customer Data
            serializer = CustomerSerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid()
            serializer.save()

            customer_id = serializer.data["id"]

            #Save Bill Data
            billData = {}
            billData["customer_id"] = customer_id
            serializer2 = BillSerialiazer(data = billData, context = {"request": request})
            serializer2.is_valid()
            serializer2.save()

            bill_id = serializer2.data["id"]
            # Access the serializer ID which just save in our db table
            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                medicine_detail1 = {}
                medicine_detail1["medicine_id"] = medicine_detail["id"]
                medicine_detail1["bill_id"] = bill_id
                medicine_detail1["qty"] = medicine_detail["qty"]

                medicine_deduct = Medicine.objects.get(id=medicine_detail["id"])
                medicine_deduct.in_stock_total = int(medicine_deduct.in_stock_total) - int(medicine_detail["qty"])
                medicine_deduct.save()

                medicine_details_list.append(medicine_detail1)
                # print(medicine_detail)

            serializer3 = BillDetailsSerializer(data = medicine_details_list, many = True, context = {"request": request})
            serializer3.is_valid()
            serializer3.save()

            dict_response = {"error": False, "message": "Bill Generate Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Generating Bill"}
        return Response(dict_response)

class CustomerRequestViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customer_request = CustomerRequest.objects.all()
        serializer = CustomerRequestSerialiazer(customer_request, many = True, context = {"request": request})
        response_dict = {"error": False, "message": "All Customer Request Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CustomerRequestSerialiazer(data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Customer Request Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Customer Request Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = CustomerRequest.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = CustomerRequestSerialiazer(customer_request, context={"request": request})

        serializer_data = serializer.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
    
    def update(self, request, pk=None):
        try:
            queryset = CustomerRequest.objects.all()
            customer_request = get_object_or_404(queryset, pk = pk)
            serializer = CustomerRequestSerialiazer(customer_request, data = request.data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Customer Request Data"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Customer Request Data"}

        return Response(dict_response)

class HomeAPIViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customer_request = CustomerRequest.objects.all()
        customer_request_serializer = CustomerRequestSerialiazer(customer_request, many = True, context = {"request": request})

        bill_count = Bill.objects.all()
        bill_count_serializer = BillSerialiazer(bill_count, many = True, context = {"request": request})

        medicine_count = Medicine.objects.all()
        medicine_count_serializer = MedicineSerialiazer(medicine_count, many = True, context = {"request": request})
        
        company_count = Company.objects.all()
        company_count_serializer = CompanySerialiazer(company_count, many = True, context = {"request": request})
        
        employee_count = Employee.objects.all()
        employee_count_serializer = EmployeeSerialiazer(employee_count, many = True, context = {"request": request})

        bill_details = BillDetails.objects.all()
        profit_amt = 0
        sell_amt = 0
        buy_amt = 0
        total_gst = 0

        for bill in bill_details:
            buy_amt = float(buy_amt) + float(bill.medicine_id.buy_price) * int(bill.qty)
            sell_amt = float(sell_amt) + (float(bill.medicine_id.sell_price) + float(bill.medicine_id.gst)) * int(bill.qty)
            total_gst = float(total_gst) + float(bill.medicine_id.gst) * int(bill.qty)
        profit_amt = sell_amt - buy_amt - total_gst

        customer_request_pending = CustomerRequest.objects.filter(status=False)
        customer_request_pending_serializer = CustomerRequestSerialiazer(customer_request_pending, many = True, context = {"request": request})

        customer_request_completed = CustomerRequest.objects.filter(status=True)
        customer_request_completed_serializer = CustomerRequestSerialiazer(customer_request_completed, many = True, context = {"request": request})

        current_date = datetime.today().strftime("%Y-%m-%d")
        # date = datetime.today()
        # current_date = date + timedelta(days=1)
        # current_date = current_date.strftime("%Y-%m-%d")
        current_date1 = datetime.today()
        current_date_7_days = current_date1 + timedelta(days=7)
        current_date_7_days = current_date_7_days.strftime("%Y-%m-%d")
        bill_details_today = BillDetails.objects.filter(added_on__date=current_date)
        profit_amt_today = 0
        sell_amt_today = 0
        buy_amt_today = 0
        total_gst_today = 0

        for bill in bill_details_today:
            buy_amt_today = float(buy_amt_today) + float(bill.medicine_id.buy_price) * int(bill.qty)
            sell_amt_today = float(sell_amt_today) + (float(bill.medicine_id.sell_price) + float(bill.medicine_id.gst)) * int(bill.qty)
            total_gst_today = float(total_gst_today) + float(bill.medicine_id.gst) * int(bill.qty)
        profit_amt_today = sell_amt_today - buy_amt_today - total_gst_today

        medicine_expire = Medicine.objects.filter(expire_date__range=[current_date, current_date_7_days])
        medicine_expire_serializer = MedicineSerialiazer(medicine_expire, many = True, context = {"request": request})

        bill_dates = BillDetails.objects.order_by().values("added_on__date").distinct()
        profit_chart_list = []
        sell_chart_list = []
        buy_chart_list = []
        for bill_date in bill_dates:
            access_date = bill_date["added_on__date"]
            bill_data = BillDetails.objects.filter(added_on__date = access_date)

            profit_amt_inner = 0
            sell_amt_inner = 0
            buy_amt_inner = 0
            gst_amt_inner = 0
            
            for billsingle in bill_data:
                buy_amt_inner = float(buy_amt_inner) + float(billsingle.medicine_id.buy_price) * int(billsingle.qty)
                sell_amt_inner = float(sell_amt_inner) + (float(billsingle.medicine_id.sell_price) + float(billsingle.medicine_id.gst)) * int(billsingle.qty)
                gst_amt_inner = float(gst_amt_inner) + float(billsingle.medicine_id.gst) * int(billsingle.qty)
            profit_amt_inner = sell_amt_inner - buy_amt_inner - gst_amt_inner

            profit_chart_list.append({"date": access_date, "amt": profit_amt_inner})
            sell_chart_list.append({"date": access_date, "amt": sell_amt_inner})
            buy_chart_list.append({"date": access_date, "amt": buy_amt_inner})


        dict_response = {"error": False, 
                        "message": "Home Page Data", 
                        "customer_request": len(customer_request_serializer.data), 
                        "bill_count": len(bill_count_serializer.data),
                        "medicine_count": len(medicine_count_serializer.data),
                        "company_count": len(company_count_serializer.data),
                        "employee_count": len(employee_count_serializer.data),
                        "sell_total": sell_amt,
                        "buy_total": buy_amt,
                        "profit_total": profit_amt,
                        "request_pending": len(customer_request_pending_serializer.data),
                        "request_completed": len(customer_request_completed_serializer.data),
                        "profit_total_today": profit_amt_today,
                        "sell_total_today": sell_amt_today,
                        "medicine_expire": len(medicine_expire_serializer.data),
                        "sell_chart": sell_chart_list,
                        "buy_chart": buy_chart_list,
                        "profit_chart": profit_chart_list
                        }
        return Response(dict_response)


company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})
# company_delete = CompanyViewSet.as_view({"delete": "delete"})