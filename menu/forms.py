from django import forms
from django.forms import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    expiration_date = forms.DateField(widget=forms.SelectDateWidget())
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), 
    	required=False, widget=forms.SelectMultiple)

    class Meta:
        model = Menu
        exclude = ('created_date',) 

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ('created_date',)         
        