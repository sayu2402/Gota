from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username,email,password=None):
        if not email:
            raise ValueError('User must have an email adress')
        
        if not username:
            raise ValueError('User must have an username')
        
        if not password:
            raise ValueError('User must have a password')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            is_active = True,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, first_name, last_name, email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password= password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_blocked = False
        user.save(using=self.db)
        return user




class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=100, unique=True)

    #required

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True


class UserOTP(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    otp = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user.username} - {self.otp}"
    
    def check_otp(self, entered_otp):
        return str(self.otp) == entered_otp