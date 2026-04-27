from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Category, Product, Order, OrderItem, Cart, Feedback

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating_display', 'created_at', 'status')
    list_filter = ('rating', 'created_at', 'product__category')
    search_fields = ('user__name', 'product__name', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'user', 'product')
    fieldsets = (
        ('Product & User', {
            'fields': ('product', 'user')
        }),
        ('Feedback Details', {
            'fields': ('rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_display(self, obj):
        rating_stars = '⭐' * obj.rating
        return f"{rating_stars} ({obj.rating}/5)"
    rating_display.short_description = 'Rating'

    def status(self, obj):
        return "✓ Active"
    status.short_description = 'Status'
