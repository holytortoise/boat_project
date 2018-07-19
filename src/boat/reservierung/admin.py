from django.contrib import admin
from .models import Boot,Reservierung,Einweisung,Images
# Register your models here.
admin.site.register(Boot)
admin.site.register(Reservierung)
admin.site.register(Einweisung)
admin.site.register(Images)
