from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

userName = "anthonyrozon1"
accessKey = "pyx1xfRY4qqkwpsEqSFM"
desired_caps = {
    'device': 'Google Pixel',
    'os_version': '7.0',
    'automationName': 'Appium',
    'app': 'bs://f2fa531a983fdf8e41eafbe701f60af30f7448af'
}

driver = webdriver.Remote(
    "http://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub",
    desired_caps
)

search_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
)
search_element.click()

search_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
)
search_input.send_keys("BrowserStack")
time.sleep(5)

search_results = driver.find_elements_by_class_name("android.widget.TextView")
assert (len(search_results) > 0)

driver.quit()
