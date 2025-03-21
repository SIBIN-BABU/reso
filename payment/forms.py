from django import forms
from.models import ShippingAdddress



class ShippingForm(forms.ModelForm):
    shipping_full_name=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}))
    shipping_email=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}))
    shipping_address1=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}))
    shipping_address2=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}))
    shipping_city=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    shipping_state=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    shipping_zipcode=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}))
    shipping_country=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
    
    
    class Meta:
        model = ShippingAdddress
        fields =['shipping_full_name','shipping_email','shipping_address1','shipping_address2','shipping_city','shipping_state','shipping_zipcode','shipping_country']
        



class CardDetails(forms.Form):
    card_name=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Holder Name'}))
    card_number=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}))
    card_exp=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' Card Experiy'}))
    card_cvv=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cvv'}))
    
