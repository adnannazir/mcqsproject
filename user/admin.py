from django.contrib import admin

from .models import CustUser


class CustUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'email_confirmed']


# Register your models here.
admin.site.register(CustUser, CustUserAdmin)
