from django.contrib import admin
from .models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'is_active', 'is_staff')
    search_fields = ('full_name', 'email')
    list_filter = ('is_active',)


class UserAppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_timestamp', 'end_timestamp', 'appointment_day')
    list_filter = ('user__email',)


admin.site.register(User, UserAdmin)
admin.site.register(UserAppointmentModel, UserAppointmentAdmin)


