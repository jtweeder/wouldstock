from django.db import models

# Create your models here.

# A model to store predictions and actuals
class Prediction(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=10)
    prediction = models.FloatField()
    actual = models.FloatField()

    def __str__(self):
        return f'Prediction: {self.prediction}, Actual: {self.actual}'
    
