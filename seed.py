import os
import django

# ตั้งค่าให้ Python รู้จัก Django Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_borrow.settings')
django.setup()

from inventory.models import Equipment

# ล้างข้อมูลเดิมออกก่อน
Equipment.objects.all().delete()

# ข้อมูลอุปกรณ์ไอทีที่ต้องการเพิ่ม
items = [
    ('MacBook Pro 16" (M2)', 'คอมพิวเตอร์/โน้ตบุ๊ก', 'AV-001', 'พร้อมใช้งาน'),
    ('Dell Latitude 5420', 'คอมพิวเตอร์/โน้ตบุ๊ก', 'AV-002', 'พร้อมใช้งาน'),
    ('iPad Pro 11" (M2)', 'แท็บเล็ต', 'TB-001', 'พร้อมใช้งาน'),
    ('iPad Air 5', 'แท็บเล็ต', 'TB-002', 'ถูกยืม'),
    ('Arduino Uno R3 Board', 'ไมโครคอนโทรลเลอร์/IoT', 'IOT-001', 'พร้อมใช้งาน'),
    ('ESP32 Wi-Fi + Bluetooth Board', 'ไมโครคอนโทรลเลอร์/IoT', 'IOT-002', 'พร้อมใช้งาน'),
    ('NodeMCU ESP8266 Board', 'ไมโครคอนโทรลเลอร์/IoT', 'IOT-003', 'พร้อมใช้งาน'),
    ('Raspberry Pi 4 Model B (8GB)', 'ไมโครคอนโทรลเลอร์/IoT', 'IOT-004', 'ส่งซ่อม'),
]

for name, category, serial, status in items:
    Equipment.objects.create(name=name, category=category, serial_number=serial, status=status)

print("-> ADDED EQUIPMENT SEEDS SUCCESSFULLY!")