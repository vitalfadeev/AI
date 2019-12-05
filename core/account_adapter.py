from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from user.models import User


class AccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login( self, request, sociallogin ):

        user = sociallogin.user

        if user.id:
            return

        if not user.Email:
            return

        try:
            user = User.objects.get(
                Email=user.Email )  # if user exists, connect the account to the existing account and login
            sociallogin.connect( request, user )
        except User.DoesNotExist:
            pass
