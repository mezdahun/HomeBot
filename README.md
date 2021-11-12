# HomeBot
Scraping ImmoSCout in given time intervals and notifying recipient via email through SMTP server

# Instructions:
 1.  Create or have a gmail account that will be used to send out emails to the recipient. The sender and recipient can be the same email address
 2.  Clone the repo
 3.  Install python 3.7 and all necessary packages with pip (seen in the import lines, such as smtplib and selenium)
4.) Install Chrome if you use a different web browser
5.) Download ChromeDriver from here: https://sites.google.com/chromium.org/driver/home
6.) unzip chromedriver to the same folder as where main.py is (only tested on windows, i.e. chromedriver.exe)
7.) change the parameters of main.py in the beginning
8.) Enable IMAP and POP on your gmail account: gmail -> setting -> all settings-> security and access
9.) Enable less secure app access in your gmail account: https://support.google.com/a/answer/6260879?hl=en
10.) run main.py
11.) eventually (in every few hours or so) you have to solve a captcha that will pop up.
12.) good luck
