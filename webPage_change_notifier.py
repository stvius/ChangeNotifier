import os
import time
import smtplib

from twilio.rest import Client
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Opening the target website a Chrome page controled by this script:

chrome_path = r"/Path/To/chromedriver" # location of chrome-webdrive
driver = webdriver.Chrome(chrome_path)
driver.delete_all_cookies() # Making sure starting on a new clean session
driver.get("https://www.Target.WebSite")

# Handling Login

LOGIN_USERNAME = os.environ.get('WEBSITE_USERNAME')
LOGIN_PASSWORD = os.environ.get('WEBSITE_PASSWORD')

# Inspect the target website and copy/paste the mentioned Login Form XPATH fields:

username =driver.find_element_by_xpath("username_XPATH") # paste the username field XPATH
username.send_keys(LOGIN_USERNAME)

password = driver.find_element_by_xpath("password_XPATH") # paste the password field XPATH
password.send_keys(LOGIN_PASSWORD)

### Handle recaptcha 

# password.send_keys(Keys.TAB + " ") # select and tick the recaptcha box
# print('\n')
# print('###########################')
# print('Pass the check for robot on Chrome to continue login')
# input("Press Enter to continue...")
# print('\n')
# print('###########################')
# print('\n')
# print('Program is running!')
# print('\n')
# print('###########################')
# print('\n')
# print('press CTRL + C to exit')

### By now, you are logged in the target web page with your credentials in a chrome page controled by this script ###


### Defining functions to notify us when a change in a web element has happened:

# Defining sending notification by whatsapp:

def send_whatsapp():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    
    client = Client(account_sid, auth_token)
    
    from_whatsapp_number = 'whatsapp:YOUR_TWILIO_NUMBER'
    to_whatsapp_number = 'whatsapp:TARGET_WHATSAPP_NUMBER'
    
    client.messages.create(body='YOUR MESSAGE HERE !',
                       from_=from_whatsapp_number, 
                       to=to_whatsapp_number)
    print('Whatsapp sent!')

# Defining sending notification by email "GMAIL":

EMAIL_ADDRESS = os.environ.get('MY_EMAIL')
EMAIL_PASSWORD = os.environ.get('MY_PASS')

msg = EmailMessage()
msg['Subject'] = 'Change Detected!'
msg['From'] = EMAIL_ADDRESS
msg['To'] =                          #  <====  PUT THE RECEIVER EMAIL HERE !
msg.set_content('*** PUT YOUR MESSAGE BODY HERE ***')

def send_mail():
    with open smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
              
         smtp.send_message(msg) 
            
         print('Email Sent!')

##################
### The app logic:
##################        

while True:
    try:
        target = driver.find_element_by_xpath('target_element_XPATH') # <== paste the targetted element's XPATH

# Handling exceptions:        

    except:
        print('Error occured... recovering...')
        driver.refresh()
        time.sleep(2)
        target = driver.find_element_by_xpath('target_element_XPATH') # <== paste the targetted element's XPATH
    
    old = int(target.text[-1])
    time.sleep(5)
    driver.refresh()
    target = driver.find_element_by_xpath('target_element_XPATH') # <== paste the targetted element's XPATH
    new = int(target.text[-1])

    if old != new:
        print('CUSTOM MESSAGE')
        send_whatsapp()
        send_mail()
