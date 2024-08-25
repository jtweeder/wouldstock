import datetime
import os
import json
import urllib.request
import ssl
import requests
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from crystalball.models import Prediction


class Command(BaseCommand):
    help = 'Make a prediction'

    
    def handle(self, *args, **options):
        
        for ticker in ["GRMN", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "INTC", "CSCO", "CAT"]:
            
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={os.getenv("PICKER")}'
            r = requests.get(url)
            data = r.json()

            #Convert Data to DataFrame
            data = pd.DataFrame(data['Time Series (Daily)']).T

            #rename columns to open, high, low, close, volume  
            data.columns = ['open', 'high', 'low', 'close', 'volume']

            #reverse the order of the dataframe
            data = data.iloc[::-1]
            data['open'] = data['open'].astype(float)
            data['high'] = data['high'].astype(float)
            data['low'] = data['low'].astype(float)
            data['close'] = data['close'].astype(float)
            data['volume'] = data['volume'].astype(float)
            columns = ['high', 'open', 'low', 'close', 'volume']
            for column in columns:
                data[f'{column}_7'] = data[column].rolling(window=7).mean()
                data[f'{column}_14'] = data[column].rolling(window=14).mean()
                data[f'{column}_21'] = data[column].rolling(window=21).mean()
                data[f'{column}_28'] = data[column].rolling(window=28).mean()

            data['Ticker'] = ticker
            
            data.dropna(inplace=True)
            data.reset_index(inplace=True)
            data.rename(columns={'index':'date'}, inplace=True)   
            
            # pull last row of each ticker
            last_row = data.iloc[-1]
            
            last_row_data = last_row.values.tolist()
            input = {
                "input_data": {
                    "columns": data.columns.tolist(),
                    "data": [last_row_data],
                    "index": [ticker]
                }
            }

            def allowSelfSignedHttps(allowed):
                # bypass the server certificate verification on client side
                if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                    ssl._create_default_https_context = ssl._create_unverified_context

            allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

            body = str.encode(json.dumps(input))
            url = 'https://stockpicker-yngfd.southcentralus.inference.ml.azure.com/score'
            api_key = os.getenv("AZUREML")
            if not api_key:
                raise Exception("A key should be provided to invoke the endpoint")

            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
            req = urllib.request.Request(url, body, headers)
            try:
                response = urllib.request.urlopen(req)

                result = response.read()
    
            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
                print(error.info())
                print(error.read().decode("utf8", 'ignore'))

            # convert bytes of result into a list
            result = result.decode("utf-8")
            result = json.loads(result)
            Prediction.objects.create(
                date = datetime.datetime.strptime(last_row['date'], '%Y-%m-%d').date(),
                ticker = ticker,
                prediction = result[0],
                close = last_row['close']
            )
           
        self.stdout.write(self.style.SUCCESS(f'Prediction saved: {Prediction}'))