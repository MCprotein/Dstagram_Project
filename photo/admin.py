from django.contrib import admin

# Register your models here.
from .models import Photo

# 어드민 페이지 옵션
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created', 'updated']
    raw_id_fields = ['author'] # 작성자 필터
    list_filter = ['created', 'updated', 'author'] # 정렬 목록 필터
    search_fields = ['text', 'created', 'author__username'] # author는 텍스트가 아니고 객체이다. ORM, API 공부할때 알아야함 __두개면 해당 모델의 하위값임
    ordering = ['-updated', '-created']

admin.site.register(Photo, PhotoAdmin)