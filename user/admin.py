from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin

# Register your models here.
# Hide ACCOUNTS / Email addresses
admin.site.unregister(EmailAddress)