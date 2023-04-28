#########################################
######### CHANGE SOME PARAMETERS ########
#########################################
import os

# Replace with the URL in browser after your desired search in ImmobilienScout24
# SEARCHURL = "https://www.immobilienscout24.de/Suche/shape/wohnung-mieten?shape=a2hoX0l3ZH5vQXVsQHl7RGRVd25DcGdDelpiXXl1QG1_QGF9RXxId2NAZEBDYENJTmRGVGdGYltrQWdAcUJsRW5BaFFfZkJ9U3tyQmVmQGFdY0x1fkhiTF9tRWlRZ31AY1lsRXN0QmRmQ3d7Q2VfQF90Q3pxQWVNb0JMZEphQnRAQGpAaWBBfFBpXmJ7QHdkQnRqRG5HaHxHaGdDeGFOanRCaHxDYkBwQGxAQGhzRHRlQQ..&numberofrooms=1.5-2.0&price=-730.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&fbclid=IwAR062sfVsI4SjJtBgjYj18dOP6I-kglSre1OSX-sNeXOKQaoOksBaFOhHHY&sorting=2"
SEARCHURL = "https://www.immobilienscout24.de/Suche/shape/wohnung-mieten?shape=Z2JvX0lveHhvQWpLb2FBfE91UGhSZUJ2fEJRdHBCcWhEZFl3fElkbkB3Z0VXe0JuV3VMaGFAcWtAaFNrU3ZIeU50SH1XY0lxXWthQHFZYVR7WmlHZUV5QGV8QG9gQGN6QUp7Q2FRd31AZE1fUXpTd2NAZkVxTmhAY0x9THFGb0VPc1FhR2NdcU5lRVltRl9dfVFvekBxZUFne0FhbEFhbEBvQ0RoRX1TbEN5XXZAbXFAZ0N3SWVFX0NtSXtAZ1J4SnVHdkp3RGpPbWFAY35BX1BpYkV5V3VJZ2JAYGxAZVV6YUN7YEJmakJ5QGlGe1FpUmFqQHhKa3hBdnhFZ3FAcnBHaUByb0JhWWRrQXlIcmBCckFoYUBySnxeZ0F2RV9FaHBBa0Z6bEBJfm5AakRqT2JSbFByRlZyTGlDXHBdfEZ8Y0BNVlhoQnJBYlxNemFAfkBqRH1CP3R5QHRwQnBhQnB8QG9CZEdhQmZOYkF0V0hgQ3NAYE99QWxFVXBVYkl6WmBEYkRsQ1Z_TWtIdklrT2JJcV1wQW1Mek5_U2xgQXZOcVRoa0NkSHx4QA..&numberofrooms=1.0-3.0&price=-950.0&livingspace=35.0-&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&sorting=2&enteredFrom=result_list&viewMode=MAP#/?boundingBox=52.353738%2C13.011954%2C52.658002%2C13.780996"
# GMail user of sender
GMAIL_USER = 'example@gmail.com'
# To use the bot generate an app password for the senders gmail account (https://myaccount.google.com/apppasswords) and copy here
GMAIL_PASSWORD = 'generated_app_password'
# The recipient and sender can be the same
RECIPIENT_EMAIL = "recipient@gmail.com"

## Google Chrome Path
# e.g. on Windows "C:\Program Files\Google\Chrome Beta\Application\chrome.exe" for Beta if installed. Leave empty if
# using normal version
CHROME_PATH = ""

# some folder where selenium can save some temporary data.
SELENIUM_ENVIRONMENT_DIR = "C:\environments\selenium"

#########################################
######## Don't Touch below ##############
#########################################

SENT_EXPOSES = []

import smtplib
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.message import EmailMessage
import random
import html_tools
import socket
from string import digits
from test_captcha import trick_captcha_if_nec
from selenium.webdriver.common.by import By

def get_local_ip_address():
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # connect to any remote server just to get the local IP address
    s.connect(('8.8.8.8', 80))

    # get the local IP address of the socket
    ip_address = s.getsockname()[0]

    # close the socket
    s.close()

    return ip_address


def scrape_expose_ids(SearchUrl=None, CAPTCHA_timeout=2, headless=True):
    """Scraping expose ids and returning most recent one"""
    if SearchUrl is None:
        SearchUrl = SEARCHURL

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("headless")
    chrome_options.add_argument(f"user-data-dir={SELENIUM_ENVIRONMENT_DIR}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")

    if CHROME_PATH != "":
        chrome_options.binary_location = CHROME_PATH

    browser = webdriver.Chrome(chrome_options=chrome_options)
    str1 = browser.capabilities['browserVersion']
    str2 = browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print(f"VERSIONS: Chrome - {str1}, ChromeDriver - {str2}")

    browser.get(SearchUrl)
    browser.implicitly_wait(3)
    try:
        radar_btn = browser.find_element(By.CSS_SELECTOR, 'div[class="geetest_radar_btn"]')
        trick_captcha_if_nec(browser)
    except:
        pass

    html_source = browser.page_source

    partitions = html_source.split("data-go-to-expose-id=")

    # expids are max 10 characters but can be shorter
    expids = [''.join(c for c in partstr[1:10] if c in digits) for partstr in partitions]
    expids.pop(0)
    uexpids = []
    for eid in expids:
        if eid not in uexpids:
            uexpids.append(eid)
            expose_url = f"https://www.immobilienscout24.de/expose/{eid}"
            if not os.path.isfile(f"htmls/expose_{eid}.html"):
                # save expose html source
                browser.get(expose_url)
                html_source = browser.page_source
                with open(f"htmls/expose_{eid}.html", "w") as f:
                    f.write(html_source)

    time.sleep(CAPTCHA_timeout)
    browser.close()
    print(uexpids)
    return uexpids


def send_expose(exp_id):
    print(f"Sending expose with id {exp_id}")

    gmail_user = GMAIL_USER
    gmail_password = GMAIL_PASSWORD
    sent_from = gmail_user

    to = [RECIPIENT_EMAIL]
    subject = '🤖🏘️ New Expose For You!'

    init_sentences = [
        "Woah, not again! A new lisiting has just arrived!",
        "Today is your lucky day! You can do this!",
        "What a lucky day is today! Another listing...",
        "Match! Match! Match!",
        "Woohoooo, a new listing is waiting for you!",
        "New day, new possibilities! I found something for you!",
        "You must have a really good Karma! Look what I have found for you...",
        "Listing alert! 🚨🚨🚨",
        "Woohoo, ImmoScout is on 🔥 today! Look what I've found...",
        "Maybe this is your new 🏘️?",
        "Look at this beauty I found for you!",
        "Who said a robot has no feelings? I - for example - am simply in ❤ with this new listing.",
        "Hang in there, your lucky day is just around the corner!",
        "How would your plants like this new apartment I found? 🌿",
        "Listings, on listings, on listings... What a day!",
        "I need no human 🧠 to guess that you might like the listing I found.",
        "Never give up! Your new 🏘️ is looking for you as desperately as you do. But soon you will find each other! ❤",
        "Yet another one? Lucky you! 🍀",
        "I'm crossing my fingers with this one! 🤞⬇",
        "You know what they say: With autumn wind comes a new home... (Okay maybe they don't say this, but it IS true!)",
        "A home is like a friend. Everyone needs one, and it is pretty difficult to find one on ImmoScout. But hey, I found a good candidate! "
    ]

    email_text = f"""\
        Dearest Recipient,

        {random.choice(init_sentences)}
        
        Short Overview:
        {html_tools.generate_html_summary(exp_id)}

        Check it out under https://www.immobilienscout24.de/expose/{exp_id}
        
        If you like the expose, you can generate an application text 
        from the local network here: http://{get_local_ip_address()}:5050/id?id={exp_id}
    

        XX,
        Your HomeBot 🤖🏘️
        """

    msg = EmailMessage()
    msg.set_content(email_text)

    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = to

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.command_encoding = 'utf-8'
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.close()
    print('Message Sent!')


def check_for_new_exposes(uexpids):
    global SENT_EXPOSES

    if SENT_EXPOSES == []:
        print('Initializing old expose database upon start...')
        SENT_EXPOSES = uexpids
        return

    for i, expid in enumerate(uexpids):
        # if i == 0:
        #     send_expose(expid)
        if expid not in SENT_EXPOSES:
            send_expose(expid)
            SENT_EXPOSES.append(expid)
        else:
            print(f'Expose with id {expid} already sent! Skipping...')


def homeBotJob():
    print('Waking UP...')
    uexpids = scrape_expose_ids(SearchUrl=SEARCHURL)
    if uexpids == []:
        # redoing CAPTCHA
        scrape_expose_ids(SearchUrl=None, CAPTCHA_timeout=12, headless=False)
    check_for_new_exposes(uexpids)
    print('Going to SLEEP...')


if __name__ == "__main__":
    print('Starting HomeBot...')
    print('Tricking CAPTCHA first...')
    schedule.every(30).seconds.do(homeBotJob)
    print('Jobs Scheduled!')
    homeBotJob()

    while True:
        schedule.run_pending()
        time.sleep(1)
