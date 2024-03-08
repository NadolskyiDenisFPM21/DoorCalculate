from django.contrib import admin

from .models import DoorBlock, Frame, Table

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

class ProductResource(resources.ModelResource):
    
    class Meta:
        model = DoorBlock


@admin.register(DoorBlock)
class DoorBlockAdmin(ImportExportActionModelAdmin):
    resource_class = ""
    list_display = ('id', 'model', 'width', 'height', 'price')
    
@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'depth', 'width_back_indent')
    


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display= ('id', 'html')