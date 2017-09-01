from django.contrib import admin
from hostlist import models
# Register your models here.

class IdcAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'idc_name', 'idc_operators', 'idc_location', 'idc_contacts', 'remark')

class MaintainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

class HostListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'status', 'idc', 'maintainer')

class HostAssetAdmin(admin.ModelAdmin):
    list_display = ('ip', 'hostname', 'macaddress', 'os', 'virtual')

admin.site.register(models.IdcAsset,IdcAssetAdmin)
admin.site.register(models.Maintainer,MaintainerAdmin)
admin.site.register(models.HostList,HostListAdmin)
admin.site.register(models.HostAsset,HostAssetAdmin)
