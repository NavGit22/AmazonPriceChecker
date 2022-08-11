import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import pandas

my_email_gmail = '****.****@****.com'
password = '********'
to_email = '****.****@****.com'

input_data = pandas.read_csv('price_checker.csv')

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/100.0.4896.127 Safari/537.36'

accept_lang = 'en-US,en;q=0.9'

headers = {
    'Accept-Language' : accept_lang,
    'User-Agent' : user_agent
}

for index, data in input_data.iterrows():
    response = requests.get(url=data['URL'], headers=headers)
    web_data = response.text

    soup = BeautifulSoup(web_data, "lxml")
    text = soup.find(name='span', class_='a-offscreen').getText()

    price = float(text.split('₹')[1].replace(',', ''))

    if price < data['Price Limit']:
        # connecting to Server provider
        with smtplib.SMTP("smtp.gmail.com") as connection_gmail:
            # Secure the connection
            connection_gmail.starttls()
            # Login to Email Provider
            connection_gmail.login(user=my_email_gmail, password=password)
            # Send the email
            connection_gmail.sendmail(
                from_addr=my_email_gmail,
                to_addrs=to_email,
                msg=f"Subject: !!!! Low Price Alert !!!! Order Now.. Order Now..\n\n {data['URL']}"
            )
