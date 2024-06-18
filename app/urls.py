from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    SalesOrderView, UserRegisterView, ImportView, 
    ContactsView, LoginView, InvoiceView, 
    CreditNoteView, ExpensesView
)

router = SimpleRouter()
router.register('contacts', ContactsView)
router.register('sales_order', SalesOrderView)
router.register('invoice', InvoiceView)
router.register('credit_note', CreditNoteView)
router.register('expenses', ExpensesView)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('import/', ImportView.as_view(), name='import'),
    path('', include(router.urls))
]
