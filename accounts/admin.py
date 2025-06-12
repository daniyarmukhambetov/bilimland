from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_solved_count')
    
    def get_solved_count(self, obj):
        return obj.profile.solved_problems_count
    get_solved_count.short_description = 'Solved Problems'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
