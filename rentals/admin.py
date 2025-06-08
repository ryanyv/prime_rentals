from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Amenity,
    Feature,
    Property,
    PropertyImage,
    TeamMember,
    Booking,
    Payment,
    Review,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "location", "rental_type", "price_nightly", "rating")
    list_filter = ("rental_type", "amenities", "features")
    search_fields = ("title", "location")
    inlines = [PropertyImageInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "years_experience")
    search_fields = ("name", "role")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("property", "first_name", "check_in", "status")
    list_filter = ("status",)
    search_fields = ("first_name", "last_name", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking", "amount", "status", "created")
    list_filter = ("status",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("property", "user", "rating", "created")
    list_filter = ("rating",)


admin.site.register(Amenity)
admin.site.register(Feature)
