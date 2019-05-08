from django.contrib import admin

# Register your models here.
from .models import *


class NewAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)


class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', "m_time"]


admin.site.register(User)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Server)
admin.site.register(StorageDevice)
admin.site.register(SecurityDevice)
admin.site.register(BusinessUnit)
admin.site.register(Contract)
admin.site.register(CPU)
admin.site.register(Disk)
admin.site.register(EventLog)
admin.site.register(NetworkDevice)
admin.site.register(NIC)
admin.site.register(RAM)
admin.site.register(Software)
admin.site.register(Tag)
admin.site.register(NewAssetApprovalZone, NewAssetAdmin)

