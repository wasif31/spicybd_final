from django import forms
from .models import Addresses


class AddressForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = [
            # 'billing_profile',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'country',
            'city',
            'state',
            'postal_code'
        ]
