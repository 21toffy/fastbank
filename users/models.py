import uuid
import datetime as d

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True, help_text="A confirmation message would be sent to your Email"
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    class Meta(object):
        unique_together = ("email",)

    USERNAME_FIELD = "email"
    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def full_name(self):
        return "{}".format(self.email )



        # return "{} {} {}".format(self.first_name, self.last_name, )

    def __str__(self):
        return str(self.full_name())




class Account_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    account_number = models.CharField(max_length=300, null=True, blank=True)
    account_type = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    sms = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    internet_banking_id = models.CharField(max_length=100, null=True, blank=True)
    account_balance = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # _account_type = (                          #private attributes
    #       ('tier_one', 'Tier_one'),
    #       ('Ttier_two', 'Tier_two'),
    #       ('Ttier_three', 'Tier_three'),
          
    # )
    # account_type  = models.CharField(max_length=100, choices= _account_type)
 

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Profiles"