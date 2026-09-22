from django.contrib import admin
from django.contrib import messages
from .models import Booking

@admin.action(description='อนุมัติการจองที่เลือก (ตัดสต็อกอุปกรณ์อัตโนมัติ)')
def approve_bookings(modeladmin, request, queryset):
    for booking in queryset.filter(status='pending'):
        if booking.equipment.available_quantity >= booking.quantity:
            booking.equipment.available_quantity -= booking.quantity
            booking.equipment.save()
            booking.status = 'approved'
            booking.save()
            modeladmin.message_user(request, f'อนุมัติการจองเรียบร้อยแล้ว', messages.SUCCESS)
        else:
            modeladmin.message_user(request, f'อุปกรณ์ {booking.equipment.name} มีจำนวนคงเหลือไม่พอ', messages.ERROR)

@admin.action(description='ปฏิเสธการจองที่เลือก')
def reject_bookings(modeladmin, request, queryset):
    queryset.filter(status='pending').update(status='rejected')
    modeladmin.message_user(request, 'ปฏิเสธคำขอการจองเรียบร้อยแล้ว', messages.WARNING)

@admin.action(description='บันทึกการคืนอุปกรณ์ (เพิ่มสต็อกกลับคืนอัตโนมัติ)')
def return_bookings(modeladmin, request, queryset):
    for booking in queryset.filter(status='approved'):
        booking.equipment.available_quantity += booking.quantity
        booking.equipment.save()
        booking.status = 'returned'
        booking.save()
        modeladmin.message_user(request, f'รับคืนอุปกรณ์เรียบร้อยแล้ว', messages.SUCCESS)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'equipment', 'quantity', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'equipment')
    search_fields = ('user__username', 'equipment__name')
    actions = [approve_bookings, reject_bookings, return_bookings]
