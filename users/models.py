from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics/')
    sheet = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_image_url(self):
        try:
            return self.image.url
        except:
            return ''

    @property
    def get_telegram_accounts(self):
        try:
            return self.user.telegram_accounts.all()
        except:
            return ''


class TelegramAccounts(models.Model):
    STATUS_CHOICES = (
        ('v', 'Verified'),
        ('un', 'UnVerified'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="telegram_accounts")
    hash_key = models.CharField(max_length=255)
    hash_id = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='v')
    
    


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
