from django import forms
from .models import PaymentSlip

class PaymentSlipForm(forms.ModelForm):
    class Meta:
        model = PaymentSlip
        fields = ['slip']

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=250)
    city = forms.CharField(max_length=100)
