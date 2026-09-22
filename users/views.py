from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import CustomUserSerializer

User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    identifier = str(request.data.get('email', '')).strip()
    password_input = str(request.data.get('password', '')).strip()

    print(f"\n--- DEBUG LOGIN ATTEMPT ---")
    print(f"INPUT RECEIVED -> Email/Username: '{identifier}', Password: '{password_input}'")

    if not identifier or not password_input:
        return Response({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'}, status=status.HTTP_400_BAD_REQUEST)

    # ค้นหาจาก Email หรือ Username
    user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()

    if not user:
        print(f"RESULT -> User NOT FOUND for: '{identifier}'")
        return Response({'success': False, 'message': f'ไม่พบบัญชีผู้ใช้ ({identifier}) ในระบบ'}, status=status.HTTP_400_BAD_REQUEST)

    print(f"USER FOUND -> Username: '{user.username}', Email: '{user.email}', is_staff: {user.is_staff}")

    # ตรวจสอบรหัสผ่าน
    if user.check_password(password_input):
        print("PASSWORD -> MATCHED! LOGIN SUCCESS\n")
        return Response({
            'success': True,
            'is_staff': user.is_staff,
            'username': user.username,
            'email': user.email,
            'message': 'เข้าสู่ระบบสำเร็จ'
        }, status=status.HTTP_200_OK)
    else:
        print("PASSWORD -> NOT MATCHED!\n")
        return Response({'success': False, 'message': 'รหัสผ่านไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)