from django.contrib import admin
from .models import DesignRequest
from .models import DesignCategory


@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'room_type', 'status', 'customer', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['name', 'description']

@admin.register(DesignCategory)
class DesignCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']