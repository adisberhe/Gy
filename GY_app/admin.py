from django.contrib import admin
from .models import MyModel
from django.core.mail import send_mail


from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('id', 'name', 'category', 'price', 'total_sale')  



class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'message')  
    list_filter = ('created_at',) 
    search_fields = ('name', 'email') 
    ordering = ('-created_at',)  

    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at') 

    def get_readonly_fields(self, request, obj=None):
        
        return self.readonly_fields

    def message(self, obj):
        return obj.message[:200] + '...'  


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'product_price', 'quantity')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at','customer_name')
    search_fields = ('customer_name', 'customer_email')
    inlines = [OrderItemInline]

    actions = ['mark_completed']

    def mark_completed(self, request, queryset):
        for order in queryset:
            order.status = 'completed'
            order.save()
            # Send email to customer
            send_mail(
                'GY Furniture Order Completed',
                f'Dear Customer Your order {order.id} is completed and ready to be taken ',
                'shop@example.com',
                [order.customer_email],
                fail_silently=False,
            )
        self.message_user(request, "Selected orders have been marked as completed and email sent.")
    
    mark_completed.short_description = "Mark selected orders as completed"

admin.site.register(Order, OrderAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin) 
admin.site.register(MyModel)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)



