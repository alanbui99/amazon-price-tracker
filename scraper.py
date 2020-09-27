import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os
import dotenv
import random

# get user input
URL = input ("Paste the full URL of the Amazon item (https://www.amazon.com/...) : ")
desired_price = float(input ("Alert you when price falls below ... (do not enter the dollar sign $) : "))
user_email = input ("Enter your email: ")

# get 50 most common user agents from file (user agent is required to scrape Amazon)
def get_UA_strings():
    lines = open('user-agents.txt').read().splitlines()
    UAs = [line.strip().strip('"') for line in lines]
    return UAs

def check_price():
    print('Checking price...')
    user_agents = get_UA_strings()

    # send request to Amazon with different user agents until accepted
    for user_agent in user_agents:
        try:
            headers = {"User-Agent": user_agent}
            page = requests.get(URL, headers = headers)
            soup = BeautifulSoup(page.content, 'lxml')
            title = soup.find(id = "productTitle").get_text().strip()
            # break out of the loop when user agent is accepted and data returns
            break
        except: 
            # delay for 1s (to avoid getting blocked), then try with the next user agent 
            time.sleep(1)
            continue        

    valid_ids = ['priceblock_ourprice','priceblock_saleprice','priceblock_dealprice','rentPrice', ] #possible ids of html tag with item price
    for id in valid_ids:
        try:
            # extract item price
            price = soup.find(id=id).get_text()
        except:
            continue
            
    current_price = float(price[1:])
    print('Current Price: $', current_price)
    print('Desired Price: $', desired_price)
    print('LOWER:',current_price < desired_price)    

    if current_price < desired_price: #send notification email if current price drops below desired price
        details = {'item': title, 'current_price': current_price}
        send_mail(details)
    else:
        f'You will be notified by email later when the price for {title} is below ${desired_price}'




def send_mail(details):
    server = smtplib.SMTP(host = 'smtp.gmail.com',port = 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    sender_email = os.getenv('EMAIL_SENDER')
    app_password = os.getenv('APP_PASSWORD')
    server.login(sender_email, app_password)

    subject = 'Lower price for ' + details['item']
    nl = '\n'
    body = f"Price for the product is now {details['current_price']}.{nl}Check the Amazon link {URL}"

    msg = f"Subject: {subject}\n\n {body}"

    server.sendmail(sender_email, user_email,msg)

    print('HEY EMAIL HAS BEEN SENT!')

    server.quit()



if __name__ =="__main__":
    while True:
        check_price()
        # check the price again after 600s
        time.sleep(600)