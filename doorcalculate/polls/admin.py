from django.contrib import admin

from .models import DoorBlock, Frame

@admin.register(DoorBlock)
class DoorBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'model', 'width', 'height', 'opening_type', 'price')
    
@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'depth', 'width_back_indent')
    
