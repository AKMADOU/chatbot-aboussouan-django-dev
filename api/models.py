from django.db import models



# encoding: utf-8



from django.utils.translation import ugettext as _

from django.db import models

# Create your models here.

from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


from datetime import date, datetime, timedelta
from django.utils.timezone import now    

from django.conf import settings


from django.urls import reverse

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, ):
    email = models.EmailField(unique=True)
    user_name = models.CharField(_('last name'), max_length=1000, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    password_reset_count = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)
    is_staff = models.BooleanField(default=False)
    

    
    objects = UserManager()

    
    USERNAME_FIELD = 'email'
    # these field are required on registering

    class Meta:
        
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return str(self.email) + ''

# Create your models here.

class Url(models.Model):
    url=models.CharField(max_length=10255)
    
    Date=models.DateField(auto_now_add=True)
    


   


    

    class Meta:
        verbose_name='url'
        verbose_name_plural='urls'









    


    
