import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = input ("Paste the full URL of the Amazon item (https://www.amazon.com/...) : ")
desired_price = input ("Alert you when price falls below ... (do not enter the dollar sign $) : ")
user_email = input ("Enter your email: ")
user_agent = input("Google search 'my user agent' and paste it here: ")

headers = {'User-Agent':user_agent}

def check_price():

    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, 'lxml')

    title = soup.find(id = "productTitle").get_text().strip()
    
    valid_ids = ['priceblock_ourprice','priceblock_saleprice','priceblock_dealprice']
    for id in valid_ids:
        try:
            price = soup.find(id=id).get_text()
        except:
            continue
    
    convert_price = float(price[1:])    

    if convert_price < float(desired_price):
        send_mail(title)


def send_mail(title):
    server = smtplib.SMTP(host = 'smtp.gmail.com',port = 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('minhthang200399@gmail.com','fuxlqcimdawkihyy')

    subject = 'Price fell down for ' + title
    body = f"Check the Amazon link {URL}"

    msg = f"Subject: {subject}\n\n {body}"

    server.sendmail('minhthang200399@gmail.com',user_email,msg)

    print('HEY EMAIL HAS BEEN SENT!')

    server.quit()



if __name__ =="__main__":
    while True:
        check_price()
        time.sleep(600)





