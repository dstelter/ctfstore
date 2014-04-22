

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from store.models import *

class CtfUserInline(admin.StackedInline):
    model = CtfUser
    can_delete = False

class CtfUserAdmin(UserAdmin):
    inlines = (CtfUserInline, )

class AchievementAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'comment')

class AchievementLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'time')

class UpgradeOrderAdmin(admin.ModelAdmin):
	list_display = ('user', 'upgrade', 'state')

class UpgradeStateAdmin(admin.ModelAdmin):
	list_display = ('title', 'subject', 'message')

# Register your models here.
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementGroup)
admin.site.register(AchievementLink, AchievementLinkAdmin)

admin.site.register(Upgrade)
admin.site.register(UpgradeState, UpgradeStateAdmin)
admin.site.register(UpgradeOrder, UpgradeOrderAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CtfUserAdmin)