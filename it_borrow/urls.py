from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet, login_api
from inventory.views import EquipmentViewSet
from bookings.views import BookingViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_api, name='login_api'),
    path('api/', include(router.urls)),
]