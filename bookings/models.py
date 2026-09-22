import uuid
from django.db import models
from django.conf import settings
from inventory.models import Equipment

class Booking(models.Model):
    STATUS_CHOICES = (('pending', 'รออนุมัติ'), ('approved', 'อนุมัติแล้ว'), ('rejected', 'ปฏิเสธ'), ('returned', 'คืนแล้ว'), ('cancelled', 'ยกเลิก'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking {self.id} - {self.user.username}'
