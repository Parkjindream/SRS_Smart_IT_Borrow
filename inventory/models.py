from django.db import models

class Equipment(models.Model):
    # กำหนดตัวเลือกสถานะให้ชัดเจน ป้องกันการพิมพ์ผิดในฐานข้อมูล
    STATUS_CHOICES = (
        ('พร้อมใช้งาน', 'พร้อมใช้งาน'),
        ('ไม่พร้อมใช้งาน', 'ไม่พร้อมใช้งาน (ส่งซ่อม/สูญหาย)'),
    )

    name = models.CharField(max_length=255, verbose_name="ชื่ออุปกรณ์")
    category = models.CharField(max_length=100, verbose_name="หมวดหมู่")
    
    # สำคัญมาก: ใส่ unique=True เพื่อไม่ให้รหัสบาร์โค้ด/QR Code ซ้ำกันในระบบ
    serial_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="ซีเรียลนัมเบอร์/รหัส")
    
    # เพิ่มฟิลด์สำหรับรูปภาพและรายละเอียด เพื่อนำไปแสดงในหน้าเว็บ
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียดอุปกรณ์")
    image = models.ImageField(upload_to='equipment_images/', blank=True, null=True, verbose_name="รูปภาพอุปกรณ์")
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='พร้อมใช้งาน', verbose_name="สถานะ")
    available_quantity = models.IntegerField(default=1, verbose_name="จำนวนที่คงเหลือ")
    total_quantity = models.IntegerField(default=1, verbose_name="จำนวนทั้งหมด")

    class Meta:
        verbose_name = "อุปกรณ์"
        verbose_name_plural = "รายการอุปกรณ์"

    def __str__(self):
        return f"{self.name} ({self.serial_number or 'ไม่มีซีเรียล'})"

    # ---------------------------------------------------------
    # ฟังก์ชันเสริม (Methods) สำหรับจัดการลอจิกระบบยืม-คืนจริง
    # ---------------------------------------------------------
    
    def is_bookable(self):
        """ตรวจสอบว่าอุปกรณ์นี้ยังสามารถจองได้หรือไม่"""
        return self.status == 'พร้อมใช้งาน' and self.available_quantity > 0

    def decrease_stock(self):
        """เรียกใช้เมื่อแอดมินสแกน QR Code 'ปล่อยของ' เพื่อตัดสต๊อก"""
        if self.available_quantity > 0:
            self.available_quantity -= 1
            self.save()
            return True
        return False

    def increase_stock(self):
        """เรียกใช้เมื่อแอดมินสแกน QR Code 'รับคืนของ' เพื่อคืนสต๊อก"""
        if self.available_quantity < self.total_quantity:
            self.available_quantity += 1
            self.save()
            return True
        return False