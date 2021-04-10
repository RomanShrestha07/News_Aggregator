# from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from djongo import models
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from taggit.models import Tag


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
    tag = models.ManyToManyField('taggit.Tag', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class BlockedSources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=300)

    def __str__(self):
        return self.source_name


class RawNews(models.Model):
    _id = models.ObjectIdField()
    source = models.CharField(max_length=50)
    headline = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    date_time = models.CharField(max_length=255)
    content = models.JSONField()
    url = models.CharField(max_length=255)
    tags = models.JSONField()
    section = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.headline


class News(models.Model):
    source = models.CharField(max_length=50)
    news_id = models.CharField(max_length=20, unique=True)
    headline = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    date_time = models.DateField()
    content = models.JSONField()
    url = models.CharField(max_length=255)
    tags = TaggableManager()
    section = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('AggregatorApp:news-detail',
                       args=[self.date_time.year, self.date_time.month, self.date_time.day, self.news_id, self.pk])


class SavedNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=50)
    headline = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    date_time = models.DateField()
    content = models.JSONField()
    url = models.CharField(max_length=255)
    tags = TaggableManager()
    section = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.headline
