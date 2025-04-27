from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UnicodeUsernameValidator,
    UserManager,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


USERNAME_REQUIRED = settings.DJOK_USER_TYPE == "username"
EMAIL_REQUIRED = settings.DJOK_USER_TYPE.startswith("email")
if not (USERNAME_REQUIRED or EMAIL_REQUIRED):
    raise ValueError("Must set DJOK_USER_TYPE")


class OkUserManager(UserManager):
    def create_superuser(self, **kwargs):
        if "username" not in kwargs:
            kwargs["username"] = kwargs["email"]
        super().create_superuser(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A modification of the built-in Django user that:
        - switches first_name & last_name for username & full_name
        - keeps other admin-compliant options
    """

    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(_("email address"), unique=EMAIL_REQUIRED, default="")
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[username_validator] if USERNAME_REQUIRED else [],
        default="",
    )
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = OkUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username" if USERNAME_REQUIRED else "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        if EMAIL_REQUIRED and not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
