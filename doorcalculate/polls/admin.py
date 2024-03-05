from django.contrib import admin

from .models import DoorBlock, Frame, Table

@admin.register(DoorBlock)
class DoorBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'width', 'height', 'price')
    
@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'depth', 'width_back_indent')
    


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display= ('id', 'html')