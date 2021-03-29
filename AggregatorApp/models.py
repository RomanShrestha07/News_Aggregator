# from django.db import models
from django.contrib.auth.models import User
from djongo import models
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager, TagField


class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Not to Specify', 'Not to Specify')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default='Not to Specify')
    bio = models.TextField(max_length=500, blank=True)
    country = CountryField(blank_label='(Select Country)', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class AddedSources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=300)


class BlockedSources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=300)


class News(models.Model):
    _id = models.ObjectIdField()
    # news_id = models.CharField(max_length=10, null=True, blank=True)
    source = models.CharField(max_length=50)
    headline = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date_time = models.CharField(max_length=255)
    content = models.JSONField()
    url = models.CharField(max_length=255)
    tags = models.JSONField()
    orders_scraped = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.headline
