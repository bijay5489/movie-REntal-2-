from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    stock = models.PositiveIntegerField(default=0)
    checked_out = models.PositiveIntegerField(default=0)


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
