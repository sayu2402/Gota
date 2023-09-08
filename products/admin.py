from django.contrib import admin
from .models import Product, Variation , Coupon , ProductOffer , ProductGallery
# Register your models here.

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_name', 'is_available')
    prepopulated_fields = {'slug' : ('product_name',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','is_active')
    list_editable = ('is_active',)

admin.site.register(Product)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Coupon)
admin.site.register(ProductOffer)
admin.site.register(ProductGallery)
