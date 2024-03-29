from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(Email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, Email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(Email, password, **extra_fields)

    def create_superuser(self, Email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(Email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # User_ID = models.OneToOneField(DjangoUser, unique=True, on_delete=models.CASCADE)

    Email = models.EmailField(null=True, unique=True)
    FirstName = models.CharField(max_length=140, null=True)
    LastName = models.CharField(max_length=140, null=True)

    UserProfile = models.TextField(null=True, help_text="Text : describe the user (optional)" )

    IsConsultant = models.BooleanField(default=False, help_text="If user can do reply to consulting offers" )
    ConsultantProfile = models.TextField(null=True, help_text="Text : describe the user if he is consultant (optional)" )

    # rest_framework.authtoken.models.Token. Or request.auth
    @property
    def APIKey( self ): return Token.objects.get(user=self)

    IsSuperAdmin = models.BooleanField(default=False, help_text="Only for some users inside IXIOO, give all access to restricted features for IXIOO" )

    AccessPending = models.BooleanField(default=False, help_text="When a user is invited , he is 'pending' until he confirm email and accept the invitation  (this is not sure, to see how it work with django systems)" )
    AccessRevoked = models.BooleanField(default=False, help_text="When a user is removed , he is AccessRevoked=1 instead to delete the user entry (this is not sure, to see how it work with django systems)" )

    Teams = models.ManyToManyField( 'team.Team', related_name="Users" , help_text="Link ManyToMany with intermediary TABLE to table TEAM" )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'User'
        indexes = [
            # models.Index(fields=['User_ID']),
            models.Index(fields=['Email']),
            models.Index(fields=['IsSuperAdmin']),
            models.Index(fields=['AccessPending']),
            models.Index(fields=['AccessRevoked']),
        ]

    USERNAME_FIELD = 'Email'
    EMAIL_FIELD = 'Email'
    REQUIRED_FIELDS = []

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ,
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    def clean(self):
        super().clean()
        self.Email = self.__class__.objects.normalize_email(self.Email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.FirstName, self.LastName)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.FirstName

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.Email], **kwargs)

    def __str__(self):
        name = self.FirstName if self.FirstName else ''
        name += self.LastName if self.LastName else ''
        return f"{name} <{self.Email}>"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
