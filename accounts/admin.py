from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Vendor, VendorRequest


# custom user admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    ordering = ('email',)
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Role Info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(CustomUser, CustomUserAdmin)


# vendor admin
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'phone', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('full_name', 'user__email', 'phone')

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'full_name', 'phone', 'bio')
        }),
        ('Professional Info', {
            'fields': ('experience_years', 'specialization')
        }),
        ('Documents', {
            'fields': ('certificate', 'id_proof')
        }),
        ('Status', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


#  vendor request admin
@admin.register(VendorRequest)
class VendorRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')

    readonly_fields = ('created_at',)

    actions = ['approve_request', 'reject_request']

    fieldsets = (
        ('Basic Info', {
            'fields': ('full_name', 'email', 'phone', 'bio')
        }),
        ('Professional Info', {
            'fields': ('experience_years', 'specialization')
        }),
        ('Documents', {
            'fields': ('certificate', 'id_proof')
        }),
        ('Status', {
            'fields': ('status', 'admin_remark')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    #  custom actions
    def approve_request(self, request, queryset):
        queryset.update(status='approved')

    approve_request.short_description = "Approve selected requests"

    def reject_request(self, request, queryset):
        queryset.update(status='rejected')

    reject_request.short_description = "Reject selected requests"