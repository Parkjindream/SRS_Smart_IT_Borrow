from django.contrib import admin
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'serial_number', 'status', 'available_quantity', 'total_quantity')
    list_filter = ('category', 'status')
    search_fields = ('name', 'serial_number', 'category')
