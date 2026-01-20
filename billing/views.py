from django.shortcuts import render, get_object_or_404, redirect
from .models import MonthlyBill, HotelItemRate,BillItem,Item, Hotel
from .forms import MonthlyBillForm,HotelForm,ItemForm, HotelItemRateForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib import messages
from django.views.decorators.http import require_POST

import csv
from django.http import HttpResponse

def home(request):
    return render(request, 'billing/home.html')

def about(request):
    return render(request, 'billing/about.html')


def billing_list(request):
    search = request.GET.get('search', '')
    month = request.GET.get('month', '')

    bills = MonthlyBill.objects.select_related('hotel') \
        .prefetch_related('items__item') \
        .order_by('-id')

    if search:
        bills = bills.filter(hotel__name__icontains=search)

    if month:
        bills = bills.filter(month__icontains=month)

    bill_data = []

    for bill in bills:
        items_total = 0

        for item in bill.items.all():
            rate = HotelItemRate.objects.get(
                hotel=bill.hotel,
                item=item.item
            ).rate
            items_total += item.quantity * rate

        transport_total = bill.transport_total
        grand_total = items_total + transport_total

        bill_data.append({
            'bill': bill,
            'items_total': items_total,
            'transport_total': transport_total,
            'grand_total': grand_total
        })

    return render(request, 'billing/billing_list.html', {
        'bill_data': bill_data,
        'search': search,
        'month': month
    })



def export_billing_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="billing.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Hotel',
        'Month',
        'Items Total',
        'Transport Total',
        'Grand Total'
    ])

    bills = MonthlyBill.objects.select_related('hotel') \
        .prefetch_related('items__item')

    for bill in bills:
        items_total = 0

        for bill_item in bill.items.all():
            rate_obj = HotelItemRate.objects.filter(
                hotel=bill.hotel,
                item=bill_item.item
            ).first()

            rate = rate_obj.rate if rate_obj else 0
            items_total += bill_item.quantity * rate

        transport_total = bill.transport_total
        grand_total = items_total + transport_total

        writer.writerow([
            bill.hotel.name,
            bill.month,
            items_total,
            transport_total,
            grand_total
        ])

    return response


def print_bill(request, bill_id):
    bill = MonthlyBill.objects.select_related('hotel') \
        .prefetch_related('items__item') \
        .get(id=bill_id)

    item_rows = []
    items_total = 0

    for idx, bill_item in enumerate(bill.items.all(), start=1):
        rate_obj = HotelItemRate.objects.filter(
            hotel=bill.hotel,
            item=bill_item.item
        ).first()

        rate = rate_obj.rate if rate_obj else 0
        total = bill_item.quantity * rate
        items_total += total

        item_rows.append({
            'sr': idx,
            'name': bill_item.item.name,
            'qty': bill_item.quantity,
            'rate': rate,
            'total': total
        })

    transport_total = bill.transport_total
    grand_total = items_total + transport_total

    context = {
        'bill': bill,
        'items': item_rows,
        'items_total': items_total,
        'transport_total': transport_total,
        'grand_total': grand_total,
    }

    return render(request, 'billing/print_bill.html', context)



def create_bill(request):
    if request.method == 'POST':
        bill_form = MonthlyBillForm(request.POST)
        if bill_form.is_valid():
            bill = bill_form.save()

            # Get all items and quantities
            item_ids = request.POST.getlist('item')
            quantities = request.POST.getlist('quantity')

            for item_id, qty in zip(item_ids, quantities):
                if item_id and qty:
                    BillItem.objects.create(
                        bill=bill,
                        item_id=int(item_id),
                        quantity=int(qty)
                    )

            return redirect('print_bill', bill_id=bill.id)
    else:
        bill_form = MonthlyBillForm()

    return render(request, 'billing/create_bill.html', {
        'bill_form': bill_form,
        'items': Item.objects.all()
    })


def bill_pdf(request, bill_id):
    bill = MonthlyBill.objects.get(id=bill_id)

    template = get_template('billing/print_bill.html')
    html = template.render({
        'bill': bill,
        'items': bill.items.all(),
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{bill.invoice_no}.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response


def generate_invoice_number():
    year = now().year
    month = now().month

    last_bill = MonthlyBill.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).order_by('-id').first()

    if last_bill:
        last_number = int(last_bill.invoice_no.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"INV-{year}-{month:02d}-{new_number:04d}"



def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_hotel')
    else:
        form = HotelForm()

    hotels = Hotel.objects.all()

    return render(request, 'billing/add_hotel.html', {
        'form': form,
        'hotels': hotels
    })


def update_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    form = HotelForm(request.POST or None, instance=hotel)
    if form.is_valid():
        form.save()
        return redirect('add_hotel')
    return render(request, 'billing/update_hotel.html', {'form': form})


def delete_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel.delete()
    return redirect('add_hotel')



def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_item')
    else:
        form = ItemForm()

    items = Item.objects.all()

    return render(request, 'billing/add_item.html', {
        'form': form,
        'items': items
    })

def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('add_item')
    return render(request, 'billing/update_item.html', {'form': form})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('add_item')



def add_hotel_item_rate(request):
    if request.method == 'POST':
        form = HotelItemRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_hotel_item_rate')
    else:
        form = HotelItemRateForm()

    rates = HotelItemRate.objects.select_related('hotel', 'item')

    return render(request, 'billing/add_rate.html', {
        'form': form,
        'rates': rates
    })

def update_hotel_item_rate(request, pk):
    rate = get_object_or_404(HotelItemRate, pk=pk)
    form = HotelItemRateForm(request.POST or None, instance=rate)
    if form.is_valid():
        form.save()
        return redirect('add_hotel_item_rate')
    return render(request, 'billing/update_rate.html', {'form': form})

def delete_hotel_item_rate(request, pk):
    rate = get_object_or_404(HotelItemRate, pk=pk)
    rate.delete()
    return redirect('add_hotel_item_rate')

from django.db.models import Sum
from .models import MonthlyBill

def billing_summary(request):
    month = request.GET.get('month')

    bills = MonthlyBill.objects.select_related('hotel').prefetch_related('items')

    if month:
        bills = bills.filter(month=month)

    summary = []
    total_grand = 0

    for bill in bills:
        summary.append({
            'bill': bill,
            'items_total': bill.items_total,
            'transport_total': bill.transport_total,
            'grand_total': bill.grand_total
        })
        total_grand += bill.grand_total

    return render(request, 'billing/summary.html', {
        'summary': summary,
        'total_grand': total_grand,
        'selected_month': month
    })




@require_POST
def delete_bill(request, bill_id):
    bill = get_object_or_404(MonthlyBill, id=bill_id)
    invoice_no = bill.invoice_no
    bill.delete()
    messages.success(request, f"Invoice {invoice_no} deleted successfully!")
    return redirect('billing_summary')


