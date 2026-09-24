from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import View ของ Users และ Inventory ของเดิมที่คุณมี
from users.views import CustomUserViewSet, login_api, register_api
from inventory.views import EquipmentViewSet

# (ลบการ import BookingViewSet ออก เพราะเราเปลี่ยนไปใช้ระบบ QR Code/Real-time แทน)

# ตั้งค่า Router สำหรับแอปที่ใช้ ViewSet ปกติ
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'equipments', EquipmentViewSet)
# (ลบ router.register ของ bookings ออก)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API ระบบสมาชิกของเดิม
    path('api/login/', login_api, name='login_api'),
    path('api/register/', register_api, name='register_api'),
    
    # API พื้นฐานที่เชื่อมกับ DefaultRouter (users, equipments)
    path('api/', include(router.urls)),
    
    # API สำหรับระบบจอง, ส่งอีเมล, เช็กสถานะ และแอดมินสแกน QR Code (ที่เราเพิ่งสร้างใหม่)
    path('', include('bookings.urls')),
]