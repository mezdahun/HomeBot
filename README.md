# HomeBot
Scraping ImmoSCout in given time intervals and notifying recipient via email through SMTP server

# Instructions:
 1.  Create or have a gmail account that will be used to send out emails to the recipient. The sender and recipient can be the same email address.
 2.  Now you will have to generate an app password for the bot so it can access the gmail account and use it to send emails. Go to this page and set up an app password: https://myaccount.google.com/apppasswords. The app should be "Mail" and the device a "Windows Computer". Homebot is only tested on Windows 10. Save this password as you will need it later.
 3.  Install `git`if not installed, then clone the repo with `git clone https://github.com/mezdahun/HomeBot.git`
 4.  [Install python 3.7+](https://www.python.org/downloads/windows/). Then install selenium and schedule with pip (`pip install selenium schedule`)
 5.  Install Chrome if you use a different web browser. 
 6.  Check the version of your Chrome by clicking on the 3 dots in the upper right corner, then go to "settings" and click on "About Chrome". If your version is 102 or below, proceed to the next step. If your version is 103, download and install Chrome Beta from here https://www.google.com/chrome/beta/
 7.  Download ChromeDriver starting with the same number as your Chrome version from here: https://sites.google.com/chromium.org/driver/home . If you had to install Chrome beta, download a version starting with 104.
 8.  unzip chromedriver to the same folder as where main.py is (only tested on windows, i.e. chromedriver.exe)
 9.  Set your search filters on ImmoScout (area, size of apartment, price ranges, etc) click on search and copy the url from the url bar of your browser. Paste it as the `SEARCHURL` variable (1st line) in main.py. You can see an example search url there, yours should look similar.
 10.  In case you had to download Chrome Beta, change the `CHROME_PATH` variable to the path of the Chrome Beta executable. On Windows, this is "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
 11.  change the other parameters of main.py in the beginning, such as the sender and recipient email address. As a password use the password from the 2nd step.
 12.  Enable IMAP and POP on your gmail account: gmail -> setting -> all settings-> security and access
 13.  Enable less secure app access in your gmail account: https://support.google.com/a/answer/6260879?hl=en
 14.  Open a command prompt and move to the folder in which main.py is. Run main.py with `py main.py` (or can also be `python main.py` or `python3 main.py` according to your installation).
 15.  Upon starting up and eventually (in every hour or so) you have to solve a captcha that will pop up.
 16.  The script will wake up in every 30 seconds in the background, scrapes ImmoScout according to your search filter (the search url you provided) and send new listings to the desired email address from the email server you have set up in the beginning.
 17.  Good luck!
