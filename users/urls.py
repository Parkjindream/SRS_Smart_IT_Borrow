from django.urls import path
from .views import login_api

urlpatterns = [
    path('login/', login_api, name='login_api'),  # รวมกับ /api/ ด้านบน จะกลายเป็น /api/login/ พอดี
]