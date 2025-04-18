from django.contrib import admin
from .models import (
    CarBrand, Car, CarImage, 
    CarFeature, Reservation, ReservationOption, 
    UserProfile, Testimonial
)

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 3

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','year', 'fuel', 'price_per_day', 'is_available')
    list_filter = ('brand','fuel', 'is_available')
    search_fields = ('name', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CarImageInline, CarFeatureInline]

class ReservationOptionInline(admin.TabularInline):
    model = ReservationOption
    extra = 1

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car','start_date', 'end_date', 'status', 'total_price')
    list_filter = ('status',)
    search_fields = ('user__username', 'car__name')
    inlines = [ReservationOptionInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    search_fields = ('user__username', 'comment')
    actions = ['approve_testimonials']
    
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
    approve_testimonials.short_description = "Approve selected testimonials"