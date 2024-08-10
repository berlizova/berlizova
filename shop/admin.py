from django.contrib import admin
from django.utils.html import mark_safe

from .models import ProdCategory, Prod, Contacts, Staff, News


# Registering the ProdCategory model with custom admin configurations
@admin.register(ProdCategory)
class ProdCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_visible",
        "sort",
    )  # Fields to display in the list view
    list_editable = (
        "name",
        "is_visible",
        "sort",
    )  # Fields that can be edited directly in the list view
    list_filter = ("is_visible",)  # Fields to filter the list by
    search_fields = ("name",)  # Fields to search by in the admin
    prepopulated_fields = {
        "slug": ("name",)
    }  # Automatically generate the slug field based on the name


# Registering the Prod model with custom admin configurations
@admin.register(Prod)
class ProdAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "is_visible",
        "sort",
        "category",
        "photo",
    )  # Fields to display in the list view
    list_editable = (
        "price",
        "is_visible",
        "sort",
        "category",
    )  # Fields that can be edited directly in the list view
    list_filter = ("category", "is_visible")  # Fields to filter the list by
    search_fields = ("name", "description")  # Fields to search by in the admin
    fields = (
        "name",
        "description",
        "price",
        "is_visible",
        "category",
        "sort",
        "photo",
    )  # Fields to display on the detail/edit page

    def photo_src_tag(self, obj):
        """
        Returns an HTML img tag to display the product's photo in the admin interface.
        """
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50px' height='50px'")

    photo_src_tag.short_description = (
        "Photo"  # Description for the photo field in the list view
    )


# Registering the Contacts model with custom admin configurations
@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "email",
        "phone",
        "opening_days",
        "working_hours",
        "closed_days",
    )  # Fields to display in the list view
    search_fields = ("address", "email", "phone")  # Fields to search by in the admin


# Registering the Staff model with custom admin configurations
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "position",
        "is_visible",
        "photo",
    )  # Fields to display in the list view
    list_editable = (
        "position",
        "is_visible",
    )  # Fields that can be edited directly in the list view
    list_filter = ("position", "is_visible")  # Fields to filter the list by
    fields = (
        "name",
        "position",
        "photo",
        "bio",
        "is_visible",
    )  # Fields to display on the detail/edit page

    def photo_src_tag(self, obj):
        """
        Returns an HTML img tag to display the staff member's photo in the admin interface.
        """
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50px' height='50px'")

    photo_src_tag.short_description = (
        "Photo"  # Description for the photo field in the list view
    )


# Registering the News model with custom admin configurations
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
        "photo",
    )  # Fields to display in the list view
    search_fields = ("title", "content")  # Fields to search by in the admin
    fields = (
        "title",
        "content",
        "photo",
        "created_at",
    )  # Fields to display on the detail/edit page
    readonly_fields = (
        "created_at",
    )  # Fields that are read-only in the admin interface
