from django.contrib import admin

from .models import Cuser


class CuserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'type_user', 'region')

# Register your models here.
admin.site.register(Cuser, CuserAdmin)