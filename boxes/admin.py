from django.contrib import admin
from .models import *

# Register your models here.


class BoxesAdmin(admin.ModelAdmin):
    list_display = ('phonefrom', 'clientfrom')


admin.site.register(Boxes, BoxesAdmin)
admin.site.register(Region)
admin.site.register(BoxHistory)
admin.site.register(Feedback)