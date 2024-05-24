from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from dotenv import dotenv_values

config = dotenv_values('.env')

class Crawler():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = config["LOGIN_URL"]
        self.email = config["EMAIL"]
        self.password = config["PASSWORD"]
        
    def login(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        input_form = self.driver.find_element(By.NAME, "text")
        input_form.send_keys(self.email)
        input_form.send_keys(Keys.RETURN)

        password_form = self.driver.find_element(By.NAME, "password")
        password_form.send_keys(self.password)
        password_form.send_keys(Keys.RETURN)
        time.sleep(5)
        
    def get_trends(self): 
        trends = []
        section = self.driver.find_element(By.XPATH, "//section[@role='region']")
        trends_div = section.find_elements(By.XPATH, "//div[@role='link']")
        
        for el in trends_div:
            trend_element = el.find_elements(By.XPATH, "//div/div[@dir='ltr']")[0]
            trend = trend_element.find_element(By.TAG_NAME, 'span').text
            trends.append(trend)
            break
        return trends        
        
    def get_web_links(self, search_term):
        web_links = []
        self.driver.get("https://google.com")
        search_bar = self.driver.find_element(By.NAME, "q")
        
        def search_item(search_term): 
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.Return)
            time.sleep(5)
            return self.driver.find_elements(By.PARTIAL_LINK_TEXT, search_term)[0]
        
        for term in search_term:
            link_element = search_item(term)
            web_links.append(link_element.get_attribute('href'))
        
        return web_links
        
        
        
        

























# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-notifications")




# driver = webdriver.Chrome()

# driver.get(url)
# driver.implicitly_wait(10)

# email = "ebonkoisrael@gmail.com"
# password = "twitter2018@"

# input_form = driver.find_element(By.NAME, "text")
# input_form.send_keys(email)
# input_form.send_keys(Keys.RETURN)
# time.sleep(1)

# password_form = driver.find_element(By.NAME, "password")
# password_form.send_keys(password)
# password_form.send_keys(Keys.RETURN)
# time.sleep(5)
    
# section_path = "//section[@role='region']"
# section = driver.find_element(By.XPATH, section_path)

# link_at = section.find_elements(By.XPATH, "//div[@role='link']")

# trends = ["The FBI", "React", "#Rainy Day", "Tinubu"]
# for el in link_at:
#     trend = el.find_elements(By.XPATH, "//div/div[@dir='ltr']")[0]
#     trend = trend.find_element(By.TAG_NAME, 'span').text
#     trends.append(trend)
#     break
    
# for trend in trends:
#     print(trend)
#     time.sleep(10)

# def search_tool(search_term):
#     driver.get("https://google.com")
#     search_bar = driver.find_element(By.NAME, "q")
#     search_bar.send_keys(search_term)
#     search_bar.send_keys(Keys.Return)
#     time.sleep(5)
    
#     search_result_el = driver.find_elements(By.PARTIAL_LINK_TEXT, search_term)[0]
#     return search_result_el.get_attribute("href")