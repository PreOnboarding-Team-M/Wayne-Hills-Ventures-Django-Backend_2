from pyexpat import model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from core.models import BaseModel

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            age=1,
            name="admin",
            phone="010-0000-0000",
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(unique=True, max_length=255, verbose_name=_("이메일"))
    password = models.CharField(max_length=128, verbose_name=_("비밀번호"))
    name = models.CharField(max_length=255, verbose_name=_("이름"))
    phone = models.CharField(max_length=255, verbose_name=_("전화번호"))
    age = models.IntegerField(verbose_name=_("나이"))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = "users"


class LoginDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("유저"))
    login_date = models.DateTimeField(auto_now_add=True, verbose_name=_("로그인 시간"))

