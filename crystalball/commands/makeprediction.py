from django.core.management.base import BaseCommand, CommandError
import datetime

class Command(BaseCommand):
    help = 'Make a prediction'

    
    def handle(self, *args, **options):
        from crystalball.models import Prediction
        
        # Pull data from API and make a dataframe
        # TODO: Bring in the API from the POC notebook

        #return the predictions that do not have a corresponding actual and have a date more than 7 business days ago
        predictions = Prediction.objects.filter(actual__isnull=True, date__lte=datetime.datetime.now()-datetime.timedelta(days=7))
      
        for prediction in predictions:
            # check if there are 7 rows of data for the ticker in the dataframe
            # if not, continue
            # if there are, calculate the max of the next 7 days from the prediction.date
            # update the prediction with the actual
        


        
        
            prediction.save()
        self.stdout.write(self.style.SUCCESS(f'Prediction saved: {prediction}'))