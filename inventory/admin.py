from django.contrib import admin
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'available_quantity', 'total_quantity')
    list_filter = ('status', 'category')
    search_fields = ('name', 'category')
