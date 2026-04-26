from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username','get_full_name','role','district','phone']
    fieldsets = UserAdmin.fieldsets + (('Farm Info', {'fields': ('role','phone','district','village','land_area')}),)

admin.site.register(Crop)
admin.site.register(CropVariety)
admin.site.register(HarvestingGuide)
admin.site.register(CropDisease)
admin.site.register(Fertilizer)
admin.site.register(Pesticide)
admin.site.register(MandiPrice)
admin.site.register(LoanScheme)
admin.site.register(FarmDiary)
admin.site.register(LearnContent)
