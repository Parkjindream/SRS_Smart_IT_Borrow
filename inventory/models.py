from django.db import models

class Equipment(models.Model):
    STATUS_CHOICES = (('available', 'พร้อมใช้งาน'), ('maintenance', 'ส่งซ่อม'), ('out_of_stock', 'หมด'))
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    total_quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
