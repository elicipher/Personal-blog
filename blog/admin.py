from django.contrib import admin
from .models import Post , Comment , Like

# Register your models here.

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ('user_display',)  # فقط نمایش، قابل تغییر نیست
    exclude = ('user','session_key',)
    def user_display(self, obj):
        if obj.user:
            return obj.user.full_name
        return "کاربر مهمان"
    user_display.short_description = 'نام کاربر'
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title',)
    inlines = [LikeInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('post' , 'user',)



