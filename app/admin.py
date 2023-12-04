from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass 

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass

