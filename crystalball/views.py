from django.shortcuts import render
from crystalball.models import Prediction
import matplotlib
import matplotlib.pyplot as plt
import io, urllib, base64, datetime

# Create your views here.

def index(request):
    # get the unique list of tickers from prediction
    tickers = Prediction.objects.values_list('ticker', flat=True).distinct()

    return render(request, 'index.html', {'tickers': tickers})


def ticker(request, ticker):
    # Predictions for the given ticker
    # Calculate the date 90 days ago
    ninety_days_ago = datetime.date.today() - datetime.timedelta(days=90)

    # Filter predictions for the given ticker and within the past 90 days
    predictions = Prediction.objects.filter(ticker=ticker, date__gte=ninety_days_ago).order_by('-date')
   

    
    # Make plot of prediction_high, prediction_low, and close across dates
    # Use matplotlib to create a plot
    dates = [prediction.date for prediction in predictions]
    prediction_high = [prediction.prediction_high for prediction in predictions]
    prediction_low = [prediction.prediction_low for prediction in predictions]
    close = [prediction.close for prediction in predictions]
    # create a fresh plot that has nothing
    matplotlib.use('agg')    
    plt.clf()
    
    plt.plot(dates, prediction_high, label='Prediction High', linestyle='dotted', color='green')
    plt.plot(dates, prediction_low, label='Prediction Low', linestyle='dotted', color='red')
    plt.plot(dates, close, label='Close', color='black', linewidth=0.5)

 
    # make the x-axis labels vertical
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Predictions')

   # plt.legend()

    # Save the plot to a file
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    string = base64.b64encode(buffer.read())
    uri = urllib.parse.quote(string)


    # Return the file path to the template
    # Display the plot in the template
    return render(request, 'ticker.html', {'predictions': predictions, 'plot_image': uri})



