# bookings/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Booking
from inventory.models import Equipment

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    user = request.user
    
    # เช็กสิทธิ์ 1 คนต่อ 1 เครื่อง
    if Booking.objects.filter(user=user, status__in=['pending_pickup', 'active']).exists():
        return Response({'success': False, 'message': 'คุณมีรายการที่ยังไม่ส่งคืน ไม่สามารถจองเพิ่มได้'}, status=400)

    equipment = get_object_or_404(Equipment, id=request.data.get('equipment_id'), is_available=True)

    booking = Booking.objects.create(
        user=user,
        equipment=equipment,
        start_date=request.data.get('start_date'),
        end_date=request.data.get('end_date')
    )

    # ส่งอีเมลแจ้งเตือนการจองสำเร็จ
    send_mail(
        f"ยืนยันการจองอุปกรณ์สำเร็จ [รหัส: {booking.booking_ref}]",
        f"รหัสจอง: {booking.booking_ref}\nกำหนดคืน: {booking.end_date}\n\nกรุณาแสดง QR Code แก่แอดมินเพื่อสแกนรับของ",
        'admin@itborrow.com',
        [user.email]
    )

    return Response({'success': True, 'booking_ref': booking.booking_ref})

@api_view(['GET'])
def check_booking_status(request, booking_ref):
    booking = get_object_or_404(Booking, booking_ref=booking_ref)
    return Response({'status': booking.status})

@api_view(['POST'])
def admin_scan_pickup(request):
    booking = get_object_or_404(Booking, booking_ref=request.data.get('booking_ref'), status='pending_pickup')
    booking.status = 'active'
    booking.save()
    
    booking.equipment.is_available = False
    booking.equipment.save()
    return Response({'success': True, 'message': 'ปล่อยของสำเร็จ ผู้ใช้กำลังใช้งาน'})

@api_view(['POST'])
def admin_scan_return(request):
    booking = get_object_or_404(Booking, booking_ref=request.data.get('booking_ref'), status='active')
    booking.status = 'returned'
    booking.save()
    
    booking.equipment.is_available = True
    booking.equipment.save()
    return Response({'success': True, 'message': 'รับคืนสำเร็จ สิทธิ์ถูกปลดล็อกแล้ว'})