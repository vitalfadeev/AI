from allauth.account.models import EmailAddress
from django.contrib import admin

# Hide Groups
from django.contrib.auth.models import Group

from user.models import User

admin.site.unregister(Group)
admin.site.unregister(EmailAddress)


# Users list
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'Email',
        'FirstName',
        'LastName',
        'IsConsultant',
        'IsSuperAdmin',
        'AccessPending',
        'AccessRevoked',
        'is_staff',
        'is_active',
        'is_superuser',
        'id',
    ]
    readonly_fields = ('APIKey',)
    search_fields = [ 'Email', 'FirstName', 'LastName' ]

    class Meta:
        fields = ('APIKey',)

# Register your models here.
admin.site.register(User, UserAdmin)
