from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    email = models.CharField(max_length=50)


class PassHistory(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    date = models.CharField(max_length=50)


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    added_by = models.CharField(max_length=50, default="")


class Verify(models.Model):
    verify = models.CharField(max_length=50)

