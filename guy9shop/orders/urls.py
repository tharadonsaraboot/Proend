from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('upload-slip/<int:order_id>/', views.upload_payment_slip, name='upload_payment_slip'),
    path('pending-payments/', views.pending_payments, name='pending_payments'),
    path('payment-confirmation/<int:order_id>/', views.payment_confirmation, name='payment_confirmation'),
]
