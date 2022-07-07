from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import datetime

from .watermark import paste_watermark


class MyUserManager(BaseUserManager):
    def create_user(self, *, email, gender, first_name='', last_name='', image=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            gender=gender,
            image=image,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        if image:
            paste_watermark(user.image.path)
        return user


class MyUser(AbstractUser):
    image = models.ImageField('photo', upload_to='users/', blank=True, null=True)

    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]
    gender = models.IntegerField('Gender', choices=GENDER_CHOICES)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.image:
    #         paste_watermark(self.image.path)

    def __str__(self):
        return self.email


class Likes(models.Model):
    sender_id = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='+', verbose_name='Sender'
    )
    receiver_id = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='+', verbose_name='Receiver'
    )
    date = models.DateTimeField('datetime', default=datetime.datetime.now)

    def __str__(self):
        return self.sender_id.email + ' likes ' + self.receiver_id.email
