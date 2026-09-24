from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer

User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


# API สำหรับเข้าสู่ระบบ (Login)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    # รองรับการรับค่าทั้ง 'username', 'email', หรือ 'identifier' จากหน้าบ้าน
    identifier = str(
        request.data.get('username') or 
        request.data.get('email') or 
        request.data.get('identifier') or ''
    ).strip()
    
    password_input = str(request.data.get('password', '')).strip()

    if not identifier or not password_input:
        return Response({
            'success': False, 
            'message': 'กรุณากรอกชื่อผู้ใช้/อีเมล และรหัสผ่าน'
        }, status=status.HTTP_400_BAD_REQUEST)

    # ค้นหาผู้ใช้จาก Email หรือ Username (ไม่สนอักษรพิมพ์เล็ก-ใหญ่)
    user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()

    if not user:
        return Response({
            'success': False, 
            'message': 'ไม่พบบัญชีผู้ใช้นี้ในระบบ'
        }, status=status.HTTP_400_BAD_REQUEST)

    # ตรวจสอบรหัสผ่าน
    if user.check_password(password_input):
        # สร้างหรือดึง Token สำหรับใช้ยืนยันตัวตนใน API อื่นๆ
        token, _ = Token.objects.get_or_create(user=user)

        # ส่งอีเมลแจ้งเตือนการเข้าสู่ระบบ
        try:
            send_mail(
                subject='[IT Borrow] แจ้งเตือนการเข้าสู่ระบบ',
                message=f'สวัสดีคุณ {user.first_name or user.username}\n\nมีการเข้าสู่ระบบ IT Borrow สำเร็จเรียบร้อยแล้ว หากไม่ได้ทำรายการ กรุณาแจ้งผู้ดูแลระบบทันที',
                from_email=getattr(settings, 'EMAIL_HOST_USER', 'noreply@itborrow.com'),
                recipient_list=[user.email],
                fail_silently=True
            )
        except Exception as e:
            print(f"Email Notification Error: {e}")

        # ตอบกลับข้อมูลที่ครบถ้วน
        return Response({
            'success': True,
            'token': token.key,          # ส่ง Token กลับไปให้ Frontend
            'is_staff': user.is_staff,   # True = Admin, False = Student
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'message': 'เข้าสู่ระบบสำเร็จ'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False, 
            'message': 'รหัสผ่านไม่ถูกต้อง'
        }, status=status.HTTP_400_BAD_REQUEST)


# API สำหรับลงทะเบียนสมาชิกใหม่ (Register)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    email = str(request.data.get('email', '')).strip().lower()
    password = str(request.data.get('password', '')).strip()
    first_name = str(request.data.get('first_name', '')).strip()
    last_name = str(request.data.get('last_name', '')).strip()
    
    # หากไม่ได้ระบุ username มา ให้ใช้อักขระหน้าเครื่องหมาย @ ของ email
    username = str(request.data.get('username', '')).strip() or (email.split('@')[0] if email else '')

    if not email or not password or not username:
        return Response({
            'success': False, 
            'message': 'กรุณากรอกข้อมูลสำคัญให้ครบถ้วน'
        }, status=status.HTTP_400_BAD_REQUEST)

    # ตรวจสอบอีเมลซ้ำ
    if User.objects.filter(email__iexact=email).exists():
        return Response({
            'success': False, 
            'message': 'อีเมลนี้ถูกใช้งานในระบบแล้ว'
        }, status=status.HTTP_400_BAD_REQUEST)

    # ตรวจสอบ Username ซ้ำ
    if User.objects.filter(username__iexact=username).exists():
        return Response({
            'success': False, 
            'message': 'ชื่อผู้ใช้นี้ถูกใช้งานในระบบแล้ว กรุณาเปลี่ยนชื่อผู้ใช้ใหม่'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # สร้างผู้ใช้งานใหม่สำหรับนักศึกษา/ผู้ใช้ทั่วไป (is_staff = False เสมอ)
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        new_user.is_staff = False
        new_user.save()

        # สร้าง Token เตรียมไว้ให้ผู้ใช้ใหม่
        token, _ = Token.objects.get_or_create(user=new_user)

        # ส่งอีเมลต้อนรับการลงทะเบียน
        try:
            send_mail(
                subject='[IT Borrow] ยินดีต้อนรับสู่ระบบยืม-คืนอุปกรณ์',
                message=f'สวัสดีคุณ {first_name or username}\n\nการลงทะเบียนบัญชีผู้ใช้ระบบ IT Borrow สำเร็จแล้ว สามารถเข้าสู่ระบบเพื่อยืมอุปกรณ์ได้ทันที',
                from_email=getattr(settings, 'EMAIL_HOST_USER', 'noreply@itborrow.com'),
                recipient_list=[email],
                fail_silently=True
            )
        except Exception as e:
            print(f"Register Email Error: {e}")

        return Response({
            'success': True, 
            'token': token.key,
            'message': 'ลงทะเบียนสำเร็จเรียบร้อยแล้ว'
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'success': False, 
            'message': f'เกิดข้อผิดพลาดในการลงทะเบียน: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)