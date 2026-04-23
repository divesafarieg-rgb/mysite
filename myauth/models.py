from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth date")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Phone number")
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, verbose_name="Avatar")

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Создан профиль для пользователя: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()