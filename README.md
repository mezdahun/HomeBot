# HomeBot
Scraping ImmoSCout in given time intervals and notifying recipient via email through SMTP server

# Instructions:
 1.  Create or have a gmail account that will be used to send out emails to the recipient. The sender and recipient can be the same email address.
 2.  Install `git`if not installed, then clone the repo with `git clone https://github.com/mezdahun/HomeBot.git`
 3.  Install python 3.7. Then install selenium and schedule with pip (`pip install selenium schedule`)
 4.  Install Chrome if you use a different web browser. 
 5.  Check the version of your Chrome by clicking on the 3 dots in the upper right corner, then go to "settings" and click on "About Chrome". If your version is 102 or below, proceed to the next step. If your version is 103, download and install Chrome Beta from here https://www.google.com/chrome/beta/
 5.  Download ChromeDriver starting with the same number as your Chrome version from here: https://sites.google.com/chromium.org/driver/home . If you had to install Chrome beta, download a version starting with 104.
 6.  unzip chromedriver to the same folder as where main.py is (only tested on windows, i.e. chromedriver.exe)
 7.  Set your search filters on ImmoScout (area, size of apartment, price ranges, etc) click on search and copy the url from the url bar of your browser. Paste it as the `SEARCHURL` variable (1st line) in main.py. You can see an example search url there, yours should look similar.
 7.  In case you had to download Chrome Beta, change the `CHROME_PATH` variable to the path of the Chrome Beta executable. On Windows, this is "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
 7.  change the other parameters of main.py in the beginning, such as gmail credentials and the folder where selenium can save some temporary data.
 8.  Enable IMAP and POP on your gmail account: gmail -> setting -> all settings-> security and access
 9.  Enable less secure app access in your gmail account: https://support.google.com/a/answer/6260879?hl=en
 10.  run main.py
 11.  Upon starting up and eventually (in every hour or so) you have to solve a captcha that will pop up.
 12.  The script will wake up in every 30 seconds in the background, scrapes ImmoScout according to your search filter (the search url you provided) and send new listings to the desired email address from the email server you have set up in the beginning.
 13.  Good luck!
