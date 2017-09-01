from django.contrib import admin
from app01 import models
# Register your models here.

# class MessgaeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'audit_time', 'type', 'action', 'action_ip', 'content')

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('client', 'name')

class CommandAdmin(admin.ModelAdmin):
    list_display = ('cmd', 'doc', 'module')

class MinionsAdmin(admin.ModelAdmin):
    list_display = ('minion', 'grains', 'pillar', 'status')

class ResultAdmin(admin.ModelAdmin):
    list_display = ('client', 'fun', 'arg', 'tgt_type', 'jid', 'minions', 'result', 'user', 'datetime')

# admin.site.register(models.Message,MessgaeAdmin)
admin.site.register(models.Module,ModuleAdmin)
admin.site.register(models.Command,CommandAdmin)
admin.site.register(models.Minions,MinionsAdmin)
admin.site.register(models.Result,ResultAdmin)