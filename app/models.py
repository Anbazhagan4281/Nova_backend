from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Invalid Email")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        user = self.create_user(email=email, password=password, **kwargs)
        return user


class Users(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username


class Address(models.Model):
    BILLING = 'billing'
    SHIPPING = 'shipping'
    ADDRESS_TYPE_CHOICES = [
        (BILLING, 'Billing'),
        (SHIPPING, 'Shipping'),
    ]
    
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    attention = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    fax = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country} ({self.get_address_type_display()})"


class ContactPerson(models.Model):
    contact_person_id = models.CharField(max_length=100)
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    skype = models.CharField(max_length=50)
    is_primary_contact = models.BooleanField(default=False)
    enable_portal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DefaultTemplates(models.Model):
    invoice_template_id = models.CharField(max_length=100)
    estimate_template_id = models.CharField(max_length=100)
    creditnote_template_id = models.CharField(max_length=100)
    purchaseorder_template_id = models.CharField(max_length=100)
    salesorder_template_id = models.CharField(max_length=100)
    retainerinvoice_template_id = models.CharField(max_length=100)
    paymentthankyou_template_id = models.CharField(max_length=100)
    retainerinvoice_paymentthankyou_template_id = models.CharField(max_length=100)
    invoice_email_template_id = models.CharField(max_length=100)
    estimate_email_template_id = models.CharField(max_length=100)
    creditnote_email_template_id = models.CharField(max_length=100)
    purchaseorder_email_template_id = models.CharField(max_length=100)
    salesorder_email_template_id = models.CharField(max_length=100)
    retainerinvoice_email_template_id = models.CharField(max_length=100)
    paymentthankyou_email_template_id = models.CharField(max_length=100)
    retainerinvoice_paymentthankyou_email_template_id = models.CharField(max_length=100)


class CustomField(models.Model):
    index = models.IntegerField()
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label}: {self.value}"


class Contact(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    contact_id = models.CharField(max_length=100, primary_key=True)
    contact_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    has_transaction = models.BooleanField(default=False)
    contact_type = models.CharField(max_length=50)
    customer_sub_type = models.CharField(max_length=50, null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_taxable = models.BooleanField(default=False)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    tax_name = models.CharField(max_length=100, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax_authority_id = models.CharField(max_length=100, null=True, blank=True)
    tax_exemption_id = models.CharField(max_length=100, null=True, blank=True)
    tax_authority_name = models.CharField(max_length=255, null=True, blank=True)
    tax_exemption_code = models.CharField(max_length=255, null=True, blank=True)
    place_of_contact = models.CharField(max_length=50, null=True, blank=True)
    gst_no = models.CharField(max_length=50, null=True, blank=True)
    tax_treatment = models.CharField(max_length=50, null=True, blank=True)
    tax_regime = models.CharField(max_length=50, null=True, blank=True)
    legal_name = models.CharField(max_length=255, null=True, blank=True)
    is_tds_registered = models.BooleanField(default=False)
    vat_treatment = models.CharField(max_length=50, null=True, blank=True,)
    gst_treatment = models.CharField(max_length=50, null=True, blank=True)
    is_linked_with_zohocrm = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    owner_id = models.CharField(max_length=100, null=True, blank=True)
    primary_id = models.CharField(max_length=100, null=True, blank=True)
    payment_terms = models.IntegerField(null=True, blank=True)
    payment_terms_label = models.CharField(max_length=50, null=True, blank=True)
    currency_id = models.CharField(max_length=20, null=True, blank=True)
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    currency_symbol = models.CharField(max_length=5, null=True, blank=True)
    opening_balance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    outstanding_receivable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding_receivable_amount_bcy = models.DecimalField(max_digits=10, decimal_places=2)
    unused_credits_receivable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    unused_credits_receivable_amount_bcy = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    payment_reminder_enabled = models.BooleanField(default=False)
    custom_fields = models.JSONField(null=True, blank=True)
    billing_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='billing_contact', limit_choices_to={'address_type': 'billing'}, blank=True, null=True)
    shipping_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='shipping_contact', limit_choices_to={'address_type': 'shipping'}, blank=True, null=True)
    contact_persons = models.ManyToManyField(ContactPerson, related_name='contact_persons', blank=True)
    default_templates = models.OneToOneField(DefaultTemplates, on_delete=models.CASCADE, related_name='default_templates', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()

    def __str__(self):
        return self.contact_name


class Invoice(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=100, primary_key=True)
    ach_payment_initiated = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)
    invoice_number = models.CharField(max_length=100)
    is_pre_gst = models.BooleanField(default=False)
    place_of_supply = models.CharField(max_length=50, blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    gst_treatment = models.CharField(max_length=50, blank=True, null=True)
    cfdi_usage = models.CharField(max_length=100, blank=True, null=True)
    vat_treatment = models.CharField(max_length=50, blank=True, null=True)
    tax_treatment = models.CharField(max_length=50, blank=True, null=True)
    vat_reg_no = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    invoice_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    payment_terms = models.IntegerField(blank=True, null=True)
    payment_terms_label = models.CharField(max_length=50, blank=True, null=True)
    currency_id = models.CharField(max_length=20, blank=True, null=True)
    currency_code = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_discount_before_tax = models.BooleanField(default=False)
    discount_type = models.CharField(max_length=50, blank=True, null=True)
    is_inclusive_tax = models.BooleanField(default=False)
    recurring_invoice_id = models.CharField(max_length=100, blank=True, null=True)
    custom_fields = models.JSONField(null=True, blank=True)
    invoice_items = models.JSONField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number


class SalesOrder(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='sales_orders_billing', blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='sales_orders_shipping', blank=True, null=True)
    is_pre_gst = models.BooleanField(default=False)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    gst_treatment = models.CharField(max_length=50, blank=True, null=True, default='')
    place_of_supply = models.CharField(max_length=50, blank=True, null=True)
    crm_owner_id = models.CharField(max_length=100, blank=True, null=True)
    crm_custom_reference_id = models.CharField(max_length=100, blank=True, null=True)
    zcrm_potential_id = models.CharField(max_length=100, blank=True, null=True)
    vat_treatment = models.CharField(max_length=50, blank=True, null=True)
    tax_treatment = models.CharField(max_length=50, blank=True, null=True)
    is_update_customer = models.BooleanField(default=False)
    salesorder_number = models.CharField(max_length=50, unique=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    customer_name =  models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    invoice_id = models.CharField(max_length=100, blank=True, null=True)
    template_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    shipment_date = models.DateField(blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    discount = models.CharField(max_length=100, blank=True, null=True)
    is_discount_before_tax = models.BooleanField(default=False)
    discount_type = models.CharField(max_length=50, blank=True, null=True)
    salesperson_id = models.CharField(max_length=100, blank=True, null=True)
    salesperson_name = models.CharField(max_length=100, blank=True, null=True)
    merchant_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    estimate_id = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    tax_authority_id = models.CharField(max_length=100, blank=True, null=True)
    tax_authority_name = models.CharField(max_length=255, blank=True, null=True)
    tax_exemption_id = models.CharField(max_length=100, blank=True, null=True)
    tax_exemption_code = models.CharField(max_length=255, blank=True, null=True)
    avatax_exempt_no = models.CharField(max_length=100, blank=True, null=True)
    avatax_use_code = models.CharField(max_length=100, blank=True, null=True)
    is_inclusive_tax = models.BooleanField(default=False)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    adjustment_description = models.CharField(max_length=255, blank=True, null=True)
    delivery_method = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    notes_default = models.TextField(blank=True, null=True)
    terms = models.TextField(blank=True, null=True)
    terms_default = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.salesorder_number


class LineItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='line_items', on_delete=models.CASCADE)
    line_item_id = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, blank=True, null=True)
    bcy_rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_name = models.CharField(max_length=100, blank=True, null=True)
    tax_type = models.CharField(max_length=50, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    tds_tax_id = models.CharField(max_length=100, blank=True, null=True)
    tax_treatment_code = models.CharField(max_length=50, blank=True, null=True)
    is_taxable = models.BooleanField(default=False)
    product_exemption_id = models.CharField(max_length=100, blank=True, null=True)
    product_exemption_code = models.CharField(max_length=100, blank=True, null=True)
    avatax_use_code_id = models.CharField(max_length=100, blank=True, null=True)
    avatax_use_code_desc = models.CharField(max_length=255, blank=True, null=True)
    avatax_tax_code_id = models.CharField(max_length=100, blank=True, null=True)
    avatax_tax_code_desc = models.CharField(max_length=255, blank=True, null=True)
    item_total_inclusive_of_tax = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=50)
    hsn_or_sac = models.CharField(max_length=50, blank=True, null=True)
    sat_item_key_code = models.CharField(max_length=50, blank=True, null=True)
    unitkey_code = models.CharField(max_length=50, blank=True, null=True)
    is_invoiced = models.BooleanField(default=False)
    stock_on_hand = models.CharField(max_length=100, blank=True, null=True)
    image_id = models.CharField(max_length=100, blank=True, null=True)
    image_name = models.CharField(max_length=100, blank=True, null=True)
    image_type = models.CharField(max_length=50, blank=True, null=True)
    project_id = models.CharField(max_length=100, blank=True, null=True)
    project_name = models.CharField(max_length=100, blank=True, null=True)
    warehouse_id = models.CharField(max_length=100, blank=True, null=True)

class SubStatus(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='sub_statuses', on_delete=models.CASCADE)
    status_id = models.CharField(max_length=100)
    status_code = models.CharField(max_length=50)
    parent_status = models.CharField(max_length=50)
    description = models.TextField()
    display_name = models.CharField(max_length=100)
    label_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7)

class SalesOrderCustomField(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='custom_fields', on_delete=models.CASCADE)
    customfield_id = models.CharField(max_length=100)
    index = models.IntegerField()
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

class SalesOrderContactPerson(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='contact_persons', on_delete=models.CASCADE)
    contact_person = models.ForeignKey(ContactPerson, on_delete=models.CASCADE)

class CreditNote(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    creditnote_id = models.CharField(max_length=100, primary_key=True)
    is_discount_before_tax = models.BooleanField(blank=True, null=True)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, null=True, blank=True)
    refund_mode = models.CharField(max_length=255, blank=True, null=True)
    place_of_supply = models.CharField(max_length=255, blank=True, null=True)
    gst_no = models.CharField(max_length=255, null=True, blank=True)
    gst_treatment = models.CharField(max_length=255, null=True, blank=True)
    vat_treatment = models.CharField(max_length=255, null=True, blank=True)
    vat_reg_no = models.CharField(max_length=255, null=True, blank=True)
    creditnote_number = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=50)
    currency_id = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=10)
    currency_symbol = models.CharField(max_length=5, blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_viewed_by_client = models.BooleanField()
    customer_id = models.CharField(max_length=255)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_in_words = models.CharField(max_length=255, blank=True, null=True)
    total_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    refundable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customer_name =  models.CharField(max_length=100, blank=True, null=True)
    invoices = models.ForeignKey(Invoice, related_name='invoices', on_delete=models.CASCADE, blank=True, null=True)
    custom_fields = models.JSONField(null=True, blank=True)
    billing_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='creditnote_billing_address', limit_choices_to={'address_type': 'billing'}, blank=True, null=True)
    shipping_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='creditnote_shipping_address', limit_choices_to={'address_type': 'shipping'}, blank=True, null=True)
    contact_persons = models.ManyToManyField(ContactPerson, related_name='creditnote_contact_persons', blank=True)
    attachments = models.JSONField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    terms = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()

    def __str__(self):
        return self.creditnote_number
    
class Expense(models.Model):
    expense_id = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=100, null=True, blank=True)
    gst_no = models.CharField(max_length=15, null=True, blank=True)
    gst_treatment = models.CharField(max_length=100, null=True, blank=True)
    tax_treatment = models.CharField(max_length=100, null=True, blank=True)
    destination_of_supply = models.CharField(max_length=100, null=True, blank=True)
    destination_of_supply_state = models.CharField(max_length=100, null=True, blank=True)
    place_of_supply = models.CharField(max_length=100, null=True, blank=True)
    hsn_or_sac = models.CharField(max_length=100, null=True, blank=True)
    source_of_supply = models.CharField(max_length=100, null=True, blank=True)
    paid_through_account_name = models.CharField(max_length=100, null=True, blank=True)
    vat_reg_no = models.CharField(max_length=100, null=True, blank=True)
    reverse_charge_tax_id = models.CharField(max_length=100, null=True, blank=True)
    reverse_charge_tax_name = models.CharField(max_length=100, null=True, blank=True)
    reverse_charge_tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reverse_charge_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_itemized_expense = models.BooleanField(null=True, blank=True)
    is_pre_gst = models.BooleanField(null=True, blank=True)
    trip_id = models.CharField(max_length=100, null=True, blank=True)
    trip_number = models.CharField(max_length=100, null=True, blank=True)
    reverse_charge_vat_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acquisition_vat_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expense_item_id = models.CharField(max_length=100, null=True, blank=True)
    account_id = models.CharField(max_length=100, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    tax_name = models.CharField(max_length=100, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    currency_id = models.CharField(max_length=100, null=True, blank=True)
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bcy_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_inclusive_tax = models.BooleanField(null=True, blank=True)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_billable = models.BooleanField(null=True, blank=True)
    is_personal = models.BooleanField(null=True, blank=True)
    customer_id = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    expense_receipt_name = models.CharField(max_length=100, null=True, blank=True)
    expense_receipt_type = models.CharField(max_length=100, null=True, blank=True)
    last_modified_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    project_id = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    mileage_rate = models.CharField(max_length=100, null=True, blank=True)
    mileage_type = models.CharField(max_length=100, null=True, blank=True)
    expense_type = models.CharField(max_length=100, null=True, blank=True)
    start_reading = models.CharField(max_length=100, null=True, blank=True)
    end_reading = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Expense {self.expense_id} by {self.customer_name}"