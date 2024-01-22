from django.contrib import admin

from .models import DoorBlock

@admin.register(DoorBlock)
class DoorBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'model', 'width', 'height', 'opening_type', 'price')
    
