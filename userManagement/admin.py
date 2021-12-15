from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email',"court", 'first_name',)
    list_filter = ('email', 'first_name', "court",'is_active', 'is_staff')
    ordering = ('start_date',)
    list_display = ('email', 'first_name',"role","court","last_name","start_date", "password",'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email','first_name',"court","role","last_name","password","call_to_bar_number","start_date")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # formfield_overrides = {
    #     User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name',"court", 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)