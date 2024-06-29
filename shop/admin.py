from django.contrib import admin
from .models import ProdCategory, Prod, Contacts, Staff, News
from django.utils.html import mark_safe


@admin.register(ProdCategory)
class ProdCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_visible', 'sort')
    list_editable = ('name', 'is_visible', 'sort')
    list_filter = ('is_visible',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Prod)
class ProdAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_visible', 'sort', 'category', 'photo')
    list_editable = ('price', 'is_visible', 'sort', 'category')
    list_filter = ('category', 'is_visible',)
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'price', 'is_visible', 'category', 'sort', 'photo')

    def photo_src_tag(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50px' height='50px'")

    photo_src_tag.short_description = 'Photo'


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('address', 'email', 'phone', 'opening_days', 'working_hours', 'closed_days')
    search_fields = ('address', 'email', 'phone')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_visible', 'photo')
    list_editable = ('position', 'is_visible')
    list_filter = ('position', 'is_visible')
    fields = ('name', 'position', 'photo', 'bio', 'is_visible')

    def photo_src_tag(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50px' height='50px'")

    photo_src_tag.short_description = 'Photo'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'photo')
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'photo', 'created_at')
    readonly_fields = ('created_at',)
