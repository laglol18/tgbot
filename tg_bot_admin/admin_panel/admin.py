from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.TgUser)
admin.site.register(models.Services)
admin.site.register(models.TgOrders)
