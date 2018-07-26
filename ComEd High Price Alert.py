
import requests
import time
from twilio.rest import Client

account_sid = "your account sid"
auth_token = "your auth token"
client = Client(account_sid, auth_token)

five_min_api = "https://hourlypricing.comed.com/api?type=5minutefeed"

five_min_api_response = requests.get(five_min_api)

counter = 0
my_price = 0

'''Gets the current time in hh:mm format'''
def get_time():
    cur_time = (time.strftime('%I:%M'))
    return cur_time

'''Gets the minute right now.'''
def get_minutes():
    minutes = (time.strftime('%M'))
    minutes = int(minutes)
    return minutes

'''Determines how many increments of 5 have passed this hour.'''
def how_many_fives():
    y = 0
    for x in range(1,get_minutes()):
        if x%5 == 0:
            y = y + 1
    return y

for x in range(0,how_many_fives()):
    agg_price = five_min_api_response.json()[x]['price']
    agg_price = float(agg_price)
    my_price = my_price + agg_price
    x = x + 1   

my_price = my_price/x
my_price = round(my_price,1)
time_now = get_time()

my_msg = "ALERT: You may want to turn off some appliances, "
hourly_avg = ("the current hourly avg at " +  str(time_now) + " is: " \
              + str(my_price) + " kWh. ")

num_to_text = "your phone number"
threshold = 7.2

'''Task schedule the script to run every 5 minutes, if the price exceeds the
threshold, send the text:
'''
if my_price > threshold:
    client.messages.create(num_to_text, 
    body=(my_msg + str(hourly_avg)),
    from_="+your Twilio number")

def main():
    get_time()
    get_minutes()
    how_many_fives()
    
main()
    

