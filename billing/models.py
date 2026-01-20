from django.db import models
from num2words import num2words

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    transport_rate_per_trip = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class HotelItemRate(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('hotel', 'item')

    def __str__(self):
        return f"{self.hotel.name} - {self.item.name}"

class MonthlyBill(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    invoice_no = models.CharField(max_length=30, unique=True,null=True, blank=True)
    total_trips = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def transport_total(self):
        return self.total_trips * self.hotel.transport_rate_per_trip

    @property
    def items_total(self):
        return sum(item.total for item in self.items.all())

    @property
    def grand_total(self):
        return self.items_total + self.transport_total
    
    @property
    def grand_total_in_words(self):
    # 'en_IN' provides the Indian numbering system (Lakhs/Crores)
        words = num2words(self.grand_total, lang='en_IN', to='currency', currency='INR')
    # Use 'words' (the variable name), not 'self.words'
        return words.title() 

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            last_bill = MonthlyBill.objects.filter(
                month=self.month
            ).order_by('-id').first()

            if last_bill and last_bill.invoice_no:
                last_no = int(last_bill.invoice_no.split('-')[-1])
                new_no = last_no + 1
            else:
                new_no = 1

            self.invoice_no = f"{self.month}-{new_no:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hotel.name} - {self.month}"

    


class BillItem(models.Model):
    bill = models.ForeignKey(
        MonthlyBill,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()

    @property
    def rate(self):
        rate_obj = HotelItemRate.objects.filter(
            hotel=self.bill.hotel,
            item=self.item
        ).first()
        return rate_obj.rate if rate_obj else 0

    @property
    def total(self):
        return self.quantity * self.rate

