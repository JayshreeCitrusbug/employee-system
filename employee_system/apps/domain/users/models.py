from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

from ...infrastructure.models import ActivityModel

# Create your models here.
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        email,
        password,
        is_admin,
        is_active=True,
        role=None,
        **extra_fields,
    ):
        """
        Creates and saves a User with the given username, email and password.
        """

        if not email:
            raise ValueError("Err_username_not_set")

        email = self.normalize_email(email)
        user = self.model(
            email=email.lower(),
            is_active=is_active,
            is_admin=is_admin,
            **extra_fields,
        )

        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.update({"user_status": User.ACTIVE, "is_active": True})
        return self._create_user(email, password, True, **extra_fields)
    
class User(AbstractBaseUser, ActivityModel):
    ref = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alias = models.CharField(max_length=40)
    about_me = models.CharField(max_length=140),
    avatar = models.ImageField(blank=True, null=True)
    # date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField()
    is_freelancer = models.BooleanField()


    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __init__(self):
        if self.is_staff:
            self.is_freelancer = False

        elif self.is_freelancer:
            self.is_staff = False


    @staticmethod
    def ref_prefix():
        # should be a default reference if user did not provide a ref themselves
        # TODO: generate prefix from project region
        return 'USR'

    def generate_ref(self):
        """
        Generate a (unique) model reference.
        Creates a reference of the form UG0000000001
        """
        return "{}{}".format(self.ref_prefix(), format(self.pk, "07d"))

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

        if hasattr(self, "ref") and not self.ref:
            self.ref = self.generate_ref()
            self.save()

    def get_full_name(self):
        return f"{self.first_name, self.last_name}"
    
    def __str__(self):
        return "{}, {}".format(self.email, self.ref)

    class Meta:
        db_table = "users"
        ordering = ["ref", "email"]