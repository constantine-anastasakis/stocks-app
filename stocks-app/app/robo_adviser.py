#from dotenv import load_dotenv
import json
import os
import requests
from IPython import embed
import datetime

months = [None, 'Jan', 'Feb','Mar', 'Apr','May','Jun','Jly','Aug','Sep','Oct','Nov','Dec']

#load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
#api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'."

with open('api_key.txt') as fin:
    api_key = fin.read().rstrip()
#print(api_key)
#exit()

print(
"""
-----------------------------------
Welcome to ROBOT INVESTOR!

Robot Investor is an artificial intelligence bot that uses the latest market data and proprietary algorithms to make investment recommendations.

How it works:

1) Enter the stock symbol for one or more publicly-traded companies.
2) Enter "next" after the last symbol to receive data and investment recommendation.

-----------------------------------
""")


def get_stocknames():
    stocknames = []
    while True:
        stock = input("Enter stock symbol (enter 'next' after last symbol): ")
        if stock.lower() == 'next':
            break
        stock = stock.strip().upper()
        stocknames.append(stock)
    return stocknames

def create_url(symbol, api_key):
    #print('API KEY:', api_key)
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SYMBOL&apikey=APIKEY"
    url = url.replace('SYMBOL', symbol)
    url = url.replace('APIKEY', api_key)
    return url

stocknames = get_stocknames()

print("-----------------------------------")

print('You entered:', stocknames)

print("-----------------------------------")

# see: https://www.alphavantage.co/documentation/#daily
for stock_name in stocknames:
    # TODO: assemble the request url to get daily data for the given stock symbol
    url = create_url(stock_name, api_key)
    #print('URL:', url)

    # TODO: issue a "GET" request to the specified url, and store the response in a variable
    response = requests.get(url)

    #print('STATUS:', response.status_code)
    if response.status_code != 200:
        print('ERROR: invalid request for', stock_name, '\n' )
        continue

    # TODO: parse the JSON response
    response_body = json.loads(response.text)

    if 'Error Message' in response_body:
        print('ERROR getting data for', stock_name)
        print(response_body['Error Message'])
    elif 'Information' in response_body:
        print('ERROR getting data for', stock_name)
        print(response_body['Information'])
        print()
        continue

    metadata = response_body["Meta Data"]
    data = response_body["Time Series (Daily)"]
    dates = list(data)
    #print(dates)

    # write data to csv file
    fn = stock_name + '.csv'
    fout = open(fn,'w')
    print ('writing data to ', fn)
    # write the headers
    hdrs = "timestamp, open, high, low, close, volume"
    fout.write(hdrs + '\n')
    # write all of the data
    high_sum = low_sum = count = 0
    for date in dates:
        day = data[date]
        open_ = day['1. open']
        high = day['2. high']
        low  = day['3. low']
        close = day['4. close']
        vol = day['5. volume']
        data_list = [date, open_, high, low, close, vol, '\n']
        s = ','.join(data_list)
        fout.write(s)
        # sum high and low
        high_sum += float(high)
        low_sum  += float(low)
        count += 1
    fout.close()
    avg_high = high_sum / count
    avg_low =  low_sum  / count

    # print out stock data
    print(f"Stock: {stock_name}")
    now = datetime.datetime.now()
    now.year, now.month, now.day, now.hour, now.minute, now.second
    am_pm = 'am'
    hour = now.hour
    if hour >+ 12:
        am_pm = 'pm'
        if hour >= 13:
            hour -= 12
    time = str(hour) + ':' + str(now.minute) + am_pm
    month_name = months[now.month]
    day_num = str(now.day)
    year = str(now.year)
    s=f"Run at: {time} on {month_name} {day_num}, {year}"
    print(s)
    refresh_date = metadata["3. Last Refreshed"]
    print("Latest data from", refresh_date)

    latest_daily_data = data[dates[0]]
    latest_price = latest_daily_data["4. close"]
    latest_price = float(latest_price)
    latest_price_usd = "${0:,.2f}".format(latest_price)
    print('Latest close:', latest_price_usd)
    print('Average High: $%.2f' % avg_high)
    print('Average Low: $%.2f' % avg_low)

    threshold = 1.2 * avg_low
    if latest_price > threshold:
        print('Buy')
    else:
        print('Do not Buy')
    print('---------------------')

#request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&1IGXSYVQWBJ2T504=demo"

#print(request_url)
#latest_price_usd = "$100,000.00" # TODO: traverse the nested response data structure to find the latest closing price

#print(f"LATEST DAILY CLOSING PRICE FOR {symbol} IS: {latest_price_usd}")
