from django.contrib.auth.models import User
from django.db import models
# from django.utils import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)
    
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email
    

# class FriendRequest(models.Model):
#     from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(CustomUser,related_name='received_requests', on_delete=models.CASCADE)
#     is_accepted = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.from_user} -> {self.to_user} ({'Accepted' if self.is_accepted else 'Pending'})"


# class Friendship(models.Model):
#     user1 = models.ForeignKey(CustomUser, related_name='friendships_initiated', on_delete=models.CASCADE)
#     user2 = models.ForeignKey(CustomUser, related_name='friendships_received', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user1','user2')

#     def __str__(self):
#         return f'{self.user1} and {self.user2} are friends'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('from_user','to_user') # Ensure uniqueness

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}"

class Friend(models.Model):
    user = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friend_of', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"