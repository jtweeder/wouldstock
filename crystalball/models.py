from django.db import models

# Create your models here.

# A model to store predictions and actuals
class Prediction(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=10)
    prediction = models.FloatField()
    close = models.FloatField()
    actual = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return f'Prediction: {self.prediction}, Actual: {self.actual}'
    
