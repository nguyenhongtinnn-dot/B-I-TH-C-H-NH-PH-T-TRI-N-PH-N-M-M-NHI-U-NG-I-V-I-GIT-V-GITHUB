from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']  # Hiển thị cột Tiêu đề và Ngày
    list_filter = ['date']           # Thêm bộ lọc theo Thời gian
    search_fields = ['title']        # Thêm thanh Tìm kiếm theo Tiêu đề

admin.site.register(Post, PostAdmin)