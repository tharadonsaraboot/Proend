from django.contrib import admin

from accounts.models import Profile
from .models import Order, OrderItem
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def mark_as_paid(modeladmin, request, queryset):
    queryset.update(paid=True)
mark_as_paid.short_description = 'Mark selected orders as paid'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'address', 'city', 'phone_number', 'created', 'updated', 'payment_slip_link', 'status_colored']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'address', 'city']
    actions = ['make_paid', 'make_shipped', 'make_cancelled']

    def status_colored(self, obj):
        colors = {
            'pending': 'blue',
            'processing': 'orange',
            'paid': 'green',
            'shipped': 'purple',
            'cancelled': 'red',
        }
        # Ensure the status is in the colors dictionary to avoid a KeyError
        color = colors.get(obj.status, 'white')
        # Call get_status_display() to safely get the human-readable status
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'
    
    def make_paid(self, request, queryset):
        queryset.update(status='paid')
    make_paid.short_description = 'Mark selected orders as paid'
    
    def make_shipped(self, request, queryset):
        queryset.update(status='shipped')
    make_shipped.short_description = 'Mark selected orders as shipped'
    
    def make_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    make_cancelled.short_description = 'Mark selected orders as cancelled'

    def payment_slip_link(self, obj):
        if hasattr(obj, 'payment_slip'):
            return format_html('<a href="{}" target="_blank">View Slip</a>', obj.payment_slip.slip.url)
        return "No Slip"
    payment_slip_link.short_description = 'Payment Slip'

    def phone_number(self, obj):
        # Try to get the profile and phone number related to the order's user
        profile = Profile.objects.filter(user=obj.user).first()
        if profile and profile.phone:
            return profile.phone
        else:
            return 'No phone'
    phone_number.short_description = 'Phone Number'