from django.db import models


class Restaurant(models.Model):
    serves_hot_dogs = models.BooleanField(
        default=False
    )
    serves_pizza = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Restaurant {self.pk}"


class RestaurantDirector(models.Model):
    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="director"
    )
    name = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f"Director {self.name}"
