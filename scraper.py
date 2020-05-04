from user_agent import generate_user_agent
import requests
from bs4 import BeautifulSoup
import smtplib
import time 


URL = input ("Paste the full URL of the Amazon item (https://www.amazon.com/...) : ")
desired_price = input ("Alert you when price falls below ... (do not enter the dollar sign $) : ")
user_email = input ("Enter your email: ")

headers = {'User-Agent': generate_user_agent()}

def check_price():

    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title= soup.find(id = "productTitle").get_text().strip()
    price = soup.find(id = "priceblock_ourprice").get_text()
    convert_price = float(price[1:])    

    if convert_price > float(desired_price):
        send_mail()


def send_mail():
    server = smtplib.SMTP(host = 'smtp.gmail.com',port = 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('minhthang200399@gmail.com','fuxlqcimdawkihyy')

    subject = f'Price fell down !'
    body = f"Check the Amazon link {URL}"

    msg = f"Subject: {subject}\n\n {body}"

    server.sendmail('minhthang200399@gmail.com',user_email,msg)

    print('HEY EMAIL HAS BEEN SENT!')

    server.quit()



if __name__ =="__main__":
    while True:
        check_price()
        #time.sleep(3600)





