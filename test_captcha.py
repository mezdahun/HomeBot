from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pyautogui
from io import BytesIO
import time, os, random
from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException

pyautogui.MINIMUM_DURATION = 0
BROWSER_MENU_HEIGHT = 170
THRESHOLD = 100

os.makedirs('snaps', exist_ok=True)
## Google Chrome Path
# e.g. on Windows "C:\Program Files\Google\Chrome Beta\Application\chrome.exe" for Beta if installed. Leave empty if
# using normal version
# CHROME_PATH = ""
#
# # some folder where selenium can save some temporary data.
# SELENIUM_ENVIRONMENT_DIR = "/home/david"
# SEARCHURL = "https://www.immobilienscout24.de/Suche/shape/wohnung-mieten?shape=Z2JvX0lveHhvQWpLb2FBfE91UGhSZUJ2fEJRdHBCcWhEZFl3fElkbkB3Z0VXe0JuV3VMaGFAcWtAaFNrU3ZIeU50SH1XY0lxXWthQHFZYVR7WmlHZUV5QGV8QG9gQGN6QUp7Q2FRd31AZE1fUXpTd2NAZkVxTmhAY0x9THFGb0VPc1FhR2NdcU5lRVltRl9dfVFvekBxZUFne0FhbEFhbEBvQ0RoRX1TbEN5XXZAbXFAZ0N3SWVFX0NtSXtAZ1J4SnVHdkp3RGpPbWFAY35BX1BpYkV5V3VJZ2JAYGxAZVV6YUN7YEJmakJ5QGlGe1FpUmFqQHhKa3hBdnhFZ3FAcnBHaUByb0JhWWRrQXlIcmBCckFoYUBySnxeZ0F2RV9FaHBBa0Z6bEBJfm5AakRqT2JSbFByRlZyTGlDXHBdfEZ8Y0BNVlhoQnJBYlxNemFAfkBqRH1CP3R5QHRwQnBhQnB8QG9CZEdhQmZOYkF0V0hgQ3NAYE99QWxFVXBVYkl6WmBEYkRsQ1Z_TWtIdklrT2JJcV1wQW1Mek5_U2xgQXZOcVRoa0NkSHx4QA..&numberofrooms=1.0-3.0&price=-950.0&livingspace=35.0-&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&sorting=2&enteredFrom=result_list&viewMode=MAP#/?boundingBox=52.353738%2C13.011954%2C52.658002%2C13.780996"


def trick_captcha_if_nec(driver):
    try:
        # You can click [radar_btn] using Selenium, but using pyautogui is way safer
        radar_btn = driver.find_element(By.CSS_SELECTOR, 'div[class="geetest_radar_btn"]')
        radar_btn.location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, 'div[class="geetest_radar_btn"]').click()
        # pyautogui.moveTo(radar_btn.location['x'] + 50, radar_btn.location['y'] + BROWSER_MENU_HEIGHT, duration=2, tween=pyautogui.easeInOutElastic)
        # pyautogui.click(duration=0.1)
        #
        # for _ in range(10):
        #     pyautogui.scroll(-10)
        time.sleep(1.5)

        # Get images
        img_el = driver.find_element(By.CSS_SELECTOR, 'canvas[class="geetest_canvas_slice geetest_absolute"]')

        byte = img_el.screenshot_as_png
        puzzle_img = Image.open(BytesIO(byte))
        puzzle_img.save(os.path.join('snaps', f'snap_{time.time()}.png'))

        driver.execute_script(
            '''var x = document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0];
            x.style.display = 'block';
            x.style.opacity = 1'''
        )

        time.sleep(0.5)
        byte = img_el.screenshot_as_png
        complete_img = Image.open(BytesIO(byte))
        complete_img.save(os.path.join('snaps', f'snap_{time.time()}.png'))

        # Get diffenrence between puzzle and complete images and get distance between different pixels
        def get_distance(img1, img2):
            for x in range(60, img1.size[0]):
                for y in range(img1.size[1]):
                    rgb1 = img1.getpixel((x, y))
                    rgb2 = img2.getpixel((x, y))

                    diff_r = abs(rgb1[0] - rgb2[0])
                    diff_g = abs(rgb1[1] - rgb2[1])
                    diff_b = abs(rgb1[2] - rgb2[2])

                    if diff_r > THRESHOLD or diff_g > THRESHOLD or diff_b > THRESHOLD:
                        return x

        distance = get_distance(puzzle_img, complete_img) - 2# some calibration needed
        print(distance)

        # Move slide button
        slider_button = driver.find_element(By.CSS_SELECTOR, 'div[class="geetest_slider_button"]')
        print("slider button location:", slider_button.location)
        scroll = driver.execute_script('return window.scrollY;') # get scroll positon
        print("scroll position:", scroll)

        pyautogui.moveTo(slider_button.location['x']+100, slider_button.location['y'] - scroll + BROWSER_MENU_HEIGHT, duration=0.2, tween=pyautogui.easeInOutElastic)
        pyautogui.mouseDown()
        dy = random.randint(-8, 8)
        noise = random.randint(-3, 3)
        first_stride = int(distance/2) - noise
        second_stride = distance + noise - first_stride + 30
        third_stride = -30
        pyautogui.moveRel(xOffset=first_stride, yOffset=dy, duration=random.randint(25, 50) / 100, tween=pyautogui.easeInOutSine)
        pyautogui.moveRel(xOffset=second_stride, yOffset=dy, duration=random.randint(25, 50) / 100, tween=pyautogui.easeInOutSine)
        pyautogui.moveRel(xOffset=third_stride, yOffset=dy, duration=random.randint(10, 25) / 100, tween=pyautogui.easeInOutSine)

        pyautogui.mouseUp()
    except NoSuchElementException:
        print("There was no captca this time!")


# chrome_options = Options()
# if headless:
#     chrome_options.add_argument("headless")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument(f"user-data-dir={SELENIUM_ENVIRONMENT_DIR}")
#
# if CHROME_PATH != "":
#     chrome_options.binary_location = CHROME_PATH
#
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.delete_all_cookies()
#
# driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
#     "origin": '*',
#     "storageTypes": 'all',
# })
#
# driver.get(SEARCHURL)
# driver.implicitly_wait(3)
# trick_captcha_if_nec(driver)
