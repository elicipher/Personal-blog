from django.contrib import admin
from .models import Member
# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'created_at')
    search_fields = ('username', 'full_name', 'email')
    list_filter = ('created_at',)
    ordering = ("-created_at",)

    