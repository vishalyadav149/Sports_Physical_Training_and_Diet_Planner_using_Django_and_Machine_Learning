from django.db import models

# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=50)
    bf = models.IntegerField()
    lu = models.IntegerField()
    di = models.IntegerField()
    cal = models.IntegerField()
    fat = models.IntegerField()
    pro = models.IntegerField()
    sug = models.IntegerField()
    imagepath= models.CharField(default="",max_length=100)

class Exercise(models.Model):
    gender = models.CharField(max_length=10)
    bmi = models.FloatField()
    sports = models.IntegerField()
    exercise_type = models.CharField(max_length=50)
    Training = models.CharField(max_length=50)

    def __str__(self):
        return self.name


