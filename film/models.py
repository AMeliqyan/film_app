from django.contrib.auth.models import User
from django.db import models


class Gener(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=250)
    img = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=250)
    genres = models.ManyToManyField(Gener)
    date = models.IntegerField(max_length=250)
    actors = models.ManyToManyField(Actor)
    languages = models.ManyToManyField(Language)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="images/", default='')
    video = models.FileField(upload_to="videos/", default='')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
    star = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='notification')
    message = models.TextField()
