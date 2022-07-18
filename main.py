#########################################
######### CHANGE SOME PARAMETERS ########
#########################################

# Replace with the URL in browser after your desired search in ImmobilienScout24
SEARCHURL = "https://www.immobilienscout24.de/Suche/shape/wohnung-mieten?shape=a2hoX0l3ZH5vQXVsQHl7RGRVd25DcGdDelpiXXl1QG1_QGF9RXxId2NAZEBDYENJTmRGVGdGYltrQWdAcUJsRW5BaFFfZkJ9U3tyQmVmQGFdY0x1fkhiTF9tRWlRZ31AY1lsRXN0QmRmQ3d7Q2VfQF90Q3pxQWVNb0JMZEphQnRAQGpAaWBBfFBpXmJ7QHdkQnRqRG5HaHxHaGdDeGFOanRCaHxDYkBwQGxAQGhzRHRlQQ..&numberofrooms=1.5-2.0&price=-730.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&fbclid=IwAR062sfVsI4SjJtBgjYj18dOP6I-kglSre1OSX-sNeXOKQaoOksBaFOhHHY&sorting=2"

# GMail user of sender
GMAIL_USER = 'example@gmail.com'
# To use the bot generate an app password for the senders gmail account (https://myaccount.google.com/apppasswords) and copy here
GMAIL_PASSWORD = 'generated_app_password'
# The recipient and sender can be the same
RECIPIENT_EMAIL = "recipient@gmail.com"

## Google Chrome Path
# e.g. on Windows "C:\Program Files\Google\Chrome Beta\Application\chrome.exe" for Beta if installed. Leave empty if
# using normal versions
CHROME_PATH = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

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


def scrape_expose_ids(SearchUrl=None, CAPTCHA_timeout=2, headless=True):
    """Scraping expose ids and returning most recent one"""
    if SearchUrl is None:
        SearchUrl = SEARCHURL

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("headless")
    chrome_options.add_argument(f"user-data-dir={SELENIUM_ENVIRONMENT_DIR}")

    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(SearchUrl)

    html_source = browser.page_source

    partitions = html_source.split("data-go-to-expose-id=")
    expids = [partstr[1:10] for partstr in partitions]
    expids.pop(0)
    uexpids = []
    for eid in expids:
        if eid not in uexpids:
            uexpids.append(eid)

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

        Check it out under https://www.immobilienscout24.de/expose/{exp_id}

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

    for expid in uexpids:
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
