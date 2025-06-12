from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Model to extend the built-in User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def solved_problems_count(self):
        """Return the number of correctly solved problems"""
        return self.user.attempts.filter(is_correct=True).count()
    
    @property
    def total_attempts_count(self):
        """Return the total number of problem attempts"""
        return self.user.attempts.count()

# Signal to create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
