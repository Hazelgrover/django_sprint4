from django.contrib import admin
from .models import Location, Category, Room, Review

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_display = ("name", "description", "slug")
    list_filter = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_display = ("name", "description", "slug")
    list_filter = ("name",)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "category", "location", "pub_date")
    list_filter = ("is_published", "category", "location", "pub_date")
    search_fields = ("title", "description", "author__username")
    raw_id_fields = ("author",)
    date_hierarchy = "pub_date"
    readonly_fields = ("created_at",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("room", "author", "created_at", "edited_at")
    list_filter = ("author", "created_at")
    search_fields = ("text", "author__username", "room__title")
    raw_id_fields = ("author", "room")