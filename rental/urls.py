from django.urls import path

app_name = "rental"

# หมายเหตุ: ยังไม่ใส่ endpoint จริง — จะเพิ่ม ViewSet/Router ในขั้นตอนถัดไป
# (โมดูล A: Auth API, โมดูล B: Inventory API, โมดูล C/D: Booking & Pickup/Return API)
urlpatterns = [
    # path("auth/login/", LoginView.as_view()),
    # path("equipment/", EquipmentListView.as_view()),
    # path("bookings/", BookingViewSet.as_view({"get": "list", "post": "create"})),
]
