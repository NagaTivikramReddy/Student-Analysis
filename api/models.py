from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Student(models.Model):
    name = models.CharField(max_length=40)
    roll_no = models.PositiveIntegerField(unique=True)
    dob = models.DateField()
    marks = models.IntegerField(blank=True, null=True, default=0, validators=[
        MaxValueValidator(100), MinValueValidator(0)])

    def __str__(self):
        return self.name
