from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from store.models import *

class CtfUserInline(admin.StackedInline):
    model = CtfUser
    can_delete = False

class CtfUserAdmin(UserAdmin):
    inlines = (CtfUserInline, )

class AchievementLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'time')

# Register your models here.
admin.site.register(Achievement)
admin.site.register(AchievementGroup)
admin.site.register(AchievementLink, AchievementLinkAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CtfUserAdmin)