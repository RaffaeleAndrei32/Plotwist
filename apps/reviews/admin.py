from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'movie', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'movie')
    search_fields = ('title', 'text', 'user__username', 'movie__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
