from django.contrib import admin
from .models import CustomUser  # Il punto indica "cerca nel file models di questa cartella"

admin.site.register(CustomUser)