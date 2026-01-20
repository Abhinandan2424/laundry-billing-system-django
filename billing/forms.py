from django import forms
from .models import MonthlyBill, BillItem, Item, HotelItemRate, Hotel

class MonthlyBillForm(forms.ModelForm):
    class Meta:
        model = MonthlyBill
        fields = ['hotel', 'month', 'total_trips']


class BillItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.IntegerField(min_value=1)

 
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'transport_rate_per_trip', 'is_active']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name']
    
class HotelItemRateForm(forms.ModelForm):
    class Meta:
        model = HotelItemRate
        fields = ['hotel', 'item', 'rate']
