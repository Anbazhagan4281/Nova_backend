from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Contact, CreditNote, SalesOrder, Invoice, Expense

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class BaseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

class ContactSerializer(BaseSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class SalesOrderSerializer(BaseSerializer):
    class Meta:
        model = SalesOrder
        fields = "__all__"

class InvoiceSerializer(BaseSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

class ExpensesOrderSerializer(BaseSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

class CreditNoteSerializer(BaseSerializer):
    class Meta:
        model = CreditNote
        fields = "__all__"
