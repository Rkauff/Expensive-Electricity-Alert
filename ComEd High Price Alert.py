# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 23:51:26 2018

@author: Ryan
"""

import requests
import time
from twilio.rest import Client

account_sid = "your twilio sid"
auth_token = "your twilio token"
client = Client(account_sid, auth_token)

hourly_api = "https://hourlypricing.comed.com/api?type=currenthouraverage"
five_min_api = "https://hourlypricing.comed.com/api?type=5minutefeed"

hourly_api_response = requests.get(hourly_api)
five_min_api_response = requests.get(five_min_api)

five_min_price = five_min_api_response.json()[0]['price'] #The current five minute price
five_min_time = five_min_api_response.json()[0]['millisUTC'] #The current five minute time
five_min_time = int(five_min_time)/1000 #To get the Millis time to a workable format
my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(five_min_time)) #To further get the millis time readable

one_hour_price = hourly_api_response.json()[0]['price'] #The current, or realtime price
one_hour_time = hourly_api_response.json()[0]['millisUTC']

counter = 0
my_price = 0

#Gets the current time in hh:mm format
def get_time():
    cur_time = (time.strftime('%I:%M'))
    return cur_time

#Gets the minute right now.
def get_minutes():
    minutes = (time.strftime('%M'))
    minutes = int(minutes)
    return minutes

#Determines how many increments of 5 have passed this hour.
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
hourly_avg = "the current hourly avg at " +  str(time_now) + " is: " + str(my_price) + " kWh. "
price_last_hour = "The price of electricity for the previous hour is: " + str(one_hour_price) + " kWh."

num_to_text = "877-837-5309"
name_to_text = "Jenny"
threshold = 7.2

#Task schedule the script to run every 5 minutes, if the price exceeds the threshold, send the text:
if my_price > threshold:
    client.messages.create(num_to_text,
        body=(my_msg + str(hourly_avg) + str(price_last_hour)),
        from_="your twilio number")






