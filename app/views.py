from django.contrib.auth import get_user_model, authenticate
from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import (
    CreditNoteSerializer, SalesOrderSerializer, UserRegisterSerializer,
    ContactSerializer, InvoiceSerializer, ExpensesOrderSerializer
)
from .models import Contact, CreditNote, SalesOrder, Invoice, Expense
import webbrowser
import socketserver
import logging
from .helper.handler import MyHandler

User = get_user_model()

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed('User Not Found')
        token = RefreshToken.for_user(user)
        return Response({
            'username': user.username,
            'refresh': str(token),
            'access_token': str(token.access_token)
        }, status=status.HTTP_200_OK)

class BaseModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user_id=user.id)
        return queryset

    def export_to_excel(self, request, queryset, title, headers, row_data_func):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = title
        worksheet.append(headers)
        for data in queryset:
            worksheet.append(row_data_func(data))
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename={title}.xlsx'
        workbook.save(response)
        return response

class SalesOrderView(BaseModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer

    @action(detail=False, methods=['get'], url_path='export')
    def export_sales_orders(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        headers = ['ID', 'Order Number', 'Customer', 'Date Created']
        return self.export_to_excel(request, queryset, 'Sales Orders', headers, 
                                    lambda data: [data.id, data.salesorder_number, data.customer_name, data.shipment_date])

class ContactsView(BaseModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @action(detail=False, methods=['get'], url_path='export')
    def export_contacts(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        headers = ['NAME', 'COMPANY NAME', 'EMAIL', 'WORK PHONE', 'RECEIVABLES (BCY)', 'UNUSED CREDITS (BCY)']
        return self.export_to_excel(request, queryset, 'Contacts', headers, 
                                    lambda data: [data.contact_name, data.company_name, data.unused_credits_receivable_amount, data.unused_credits_receivable_amount_bcy])

class InvoiceView(BaseModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=False, methods=['get'], url_path='export')
    def export_invoices(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        headers = ['ID', 'Order Number', 'Customer', 'Date Created']
        return self.export_to_excel(request, queryset, 'Invoices', headers, 
                                    lambda data: [data.id, data.salesorder_number, data.customer_name, data.shipment_date])

class CreditNoteView(BaseModelViewSet):
    queryset = CreditNote.objects.all()
    serializer_class = CreditNoteSerializer

    @action(detail=False, methods=['get'], url_path='export')
    def export_credit_notes(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        headers = ['ID', 'Credit Note', 'Status']
        return self.export_to_excel(request, queryset, 'Credit Notes', headers, 
                                    lambda data: [data.creditnote_id, data.creditnote_number, data.status])

class ExpensesView(BaseModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpensesOrderSerializer

    @action(detail=False, methods=['get'], url_path='export')
    def export_expenses(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        headers = ['DATE', 'EXPENSE ACCOUNT', 'REFERENCE NUMBER', 'VENDOR NAME', 'PAID THROUGH', 'CUSTOMER NAME', 'STATUS', 'AMOUNT']
        return self.export_to_excel(request, queryset, 'Expenses', headers, 
                                    lambda data: [data.date, data.account_name, data.reference_number, data.paid_through_account_name, data.customer_name, data.status, data.total])

class ImportView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        client_id = request.data.get('client_id')
        client_secret = request.data.get('serect_code')
        user = request.data.get('user')
        port = 8003
        organization_id = "60030126546"
        token_url = "https://accounts.zoho.in/oauth/v2/token"
        scope = "ZohoBooks.fullaccess.all"
        redirect_uri = f"http://localhost:{port}"
        auth_url = f"https://accounts.zoho.in/oauth/v2/auth?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}&prompt=consent&access_type=offline"

        apis_to_handle = [
            {"url": "https://www.zohoapis.in/books/v3/contacts", "filename": "contacts.csv", "name": "contacts"},
            {"url": "https://www.zohoapis.in/books/v3/salesorders", "filename": "sales_orders.csv", "name": "salesorders"},
            {"url": "https://www.zohoapis.in/books/v3/invoices", "filename": "invoices.csv", "name": "invoices"},
            {"url": "https://www.zohoapis.in/books/v3/creditnotes", "filename": "creditnotes.csv", "name": "creditnotes"},
            {"url": "https://www.zohoapis.in/books/v3/expenses", "filename": "expenses.csv", "name": "expenses"},
        ]

        user = User.objects.get(username=user)
        webbrowser.open(auth_url)
        with socketserver.ThreadingTCPServer(("", port), MyHandler) as httpd:
            httpd.RequestHandlerClass.user = user
            httpd.RequestHandlerClass.client_id = client_id
            httpd.RequestHandlerClass.client_secret = client_secret
            httpd.RequestHandlerClass.redirect_uri = redirect_uri
            httpd.RequestHandlerClass.organization_id = organization_id
            httpd.RequestHandlerClass.token_url = token_url
            httpd.RequestHandlerClass.apis_to_handle = apis_to_handle

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                logging.info("Server stopped.")
        httpd.shutdown()
        httpd.server_close()
        return Response({"message": "Authorization process started."})
