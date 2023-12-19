from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import time
import os

import yaml

def read_yaml_settings(file_path):
    with open(file_path, 'r') as file:
        settings = yaml.safe_load(file)
    return settings

def send_email(subject, body, sender_email, sender_password, recipient_list, smtp_host='smtp.gmail.com', smtp_port=587):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(recipient_list)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_list, text)

    print("Email sent successfully!")


subject = 'Tesla price alert!'
body = 'Tesla price @'


# Read the YAML settings
settings = read_yaml_settings('setting.yml')

tesla_url = settings['tesla_url']
sender_email = settings['sender_email']
sender_password = settings['sender_password']
recipient_list = settings['receipient_list']

def watch_tesla():
    # test using Chrome Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)

    # Load the URL and get the page source
    driver.get(tesla_url)

    car_prices = []

    try:
        results_container = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "results-container"))
        )

        car_sections = results_container.find_elements(By.CLASS_NAME, "result-header")

        # Now you can iterate over these article elements and perform any actions you desire.
        for car_section in car_sections:
            car_price_str = car_section.find_element(By.CLASS_NAME, "result-purchase-price").get_attribute("innerHTML")
            #print(car_price_str)
            car_price = int(car_price_str.replace('$', '').replace(',', ''))
            car_prices.append(car_price)
            if car_price < int(settings['price_threshold']):
                # Example usage
                body = 'Tesla price @ ' + str(car_price)
                print(body)
                send_email(subject, body, sender_email, sender_password, recipient_list)

    finally:
        driver.quit()

    return car_prices

body = "test email"
send_email(subject, body, sender_email, sender_password, recipient_list)

try:
  while True:
    print(watch_tesla())
    time.sleep(int(settings['poll_interval_sec']))
except KeyboardInterrupt:
  print("exit")
