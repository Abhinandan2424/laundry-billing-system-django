from django.contrib import admin
from .models import Hotel, MonthlyBill, BillItem, Item, HotelItemRate

admin.site.register(Hotel)
admin.site.register(Item)
admin.site.register(HotelItemRate)
admin.site.register(MonthlyBill)
admin.site.register(BillItem)
