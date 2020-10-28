from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from subscribers.models import Subscribers


class UserInline(admin.StackedInline):
	model = Subscribers
	can_delete = False
	fk_name = 'user'
	verbose_name_plural = 'Подписчики'


class UserAdmin(UserAdmin):
	inlines = (UserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
