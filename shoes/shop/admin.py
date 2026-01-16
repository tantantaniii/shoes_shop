from django.contrib import admin
from .models import Category, Brand, Shoe, ShoeSize

class ShoeSizeInline(admin.TabularInline):
    model = ShoeSize
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'category', 'gender', 'season',
        'price', 'is_waterproof', 'created_at'
    ]
    list_filter = ['brand', 'category', 'gender', 'season', 'is_waterproof']
    search_fields = ['name', 'brand__name']
    inlines = [ShoeSizeInline]
    ordering = ['-created_at']