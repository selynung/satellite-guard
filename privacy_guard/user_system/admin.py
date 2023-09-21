from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ('get_masked_ssn',)  # Make the method read-only

admin.site.register(CustomUser, CustomUserAdmin)
