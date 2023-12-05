# models.py
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


# class CustomUserManager(UserManager):
#     def create_user_with_profile(self, username, email, password=None, **extra_fields):
#         user = self.create_user(username=username, email=email, password=password, **extra_fields)
#         UserProfile.objects.create(user=user)
#         return user

#     def create_superuser_with_profile(self, username, email, password=None, **extra_fields):
#         user = self.create_superuser(username=username, email=email, password=password, **extra_fields)
#         UserProfile.objects.create(user=user)
#         return user

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
         
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
        

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # Add any additional fields you need

    # objects = CustomUserManager()
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["role"]


    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # Add any additional fields for the profile


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    published_date = models.DateField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
