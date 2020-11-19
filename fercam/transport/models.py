from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone
from django.utils.html import mark_safe

now = date.today

class User(AbstractUser):
    likes = models.IntegerField(default=0)


class Trip(models.Model):
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    def __str__(self):
        return self.origin

    def is_valid(self):
        return self.origin != self.destination


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    distance = models.FloatField(default=0)
    duration = models.FloatField(default=0)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    scope = models.CharField(max_length=13)
    weight = models.FloatField(default=0)
    size = models.FloatField(default=0)
    time_order_was_placed = models.DateTimeField(blank=True, auto_now_add=True)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2)

    # check if the order is valid
    def is_valid(self):
        if self.weight != 0 and self.size != 0 and self.origin != self.destination:
            return True
        else:
            return False

    def __str__(self):
        return f"For {self.user.first_name}: from {self.origin} to {self.destination} | Price: {self.price}"


class Driver_pay(models.Model):
    driver = models.CharField(max_length=200)
    pay = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.driver} - Hourly Pay: {self.pay}"


class Weight_coefficient(models.Model):
    name = models.CharField(max_length=20)
    coefficient = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} - Value: {self.coefficient}"



class Size_coefficient(models.Model):
    name = models.CharField(max_length=20)
    coefficient = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} - Value: {self.coefficient}"


class Distance_coefficient(models.Model):
    name = models.CharField(max_length=20)
    coefficient = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} - Value: {self.coefficient}"


class Time_coefficient(models.Model):
    name = models.CharField(max_length=20)
    coefficient = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} - Value: {self.coefficient}"


class Cargo_picture(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="todo_picture", null=True, to_field="id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_pictures", null=True)
    cargo_picture = models.ImageField(upload_to="cargo_images", blank=True)

    # so you can see an image tag instead of a link in admin
    def image_tag(self):
        return mark_safe('<img src="/static/images/media/cargo_images/coglioni.jpg" width="150" height="150" />')

    image_tag.short_description = 'Image'

    def __str__(self):
        return mark_safe(f'<img src="/static/images/media/{self.cargo_picture}" width="40" />')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message = models.TextField()
    time = models.DateTimeField(blank=True, auto_now_add=True)
