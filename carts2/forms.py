from django import forms
from listings.models import Listing
PPRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=(PPRODUCT_QUANTITY_CHOICES), coerce=int)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        # print("hello")
        super(CartAddProductForm, self).__init__(*args, **kwargs)


class CCartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=(), coerce=int)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        print("clean", self.cleaned_data, "quantity", quantity)
        # if(quantity > 3):
        #     raise forms.ValidationError("Error!")

    def __init__(self, PRODUCT_QUANTITY_CHOICES=[(i, str(i)) for i in range(1, 26)], *args, **kwargs):

        super(CCartAddProductForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].choices = PRODUCT_QUANTITY_CHOICES
