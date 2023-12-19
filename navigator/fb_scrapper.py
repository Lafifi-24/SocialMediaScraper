from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from configue import Configue

class FBScrapper:
    
    def __init__(self, email:str, password:str):
        self.email =  email
        self.password = password
        self._prepare_envirenment()
        
    def _prepare_envirenment(self):
        self.driver = webdriver.Edge()
        try:
            self.driver.get("https://www.facebook.com/")
            sleep(10)
            
        except:
            raise ValueError("Error: Can't open facebook.com")
        
        self.driver.find_element(By.XPATH, "//input[@name='email']").send_keys(Configue.FB_email)
        self.driver.find_element(By.XPATH, "//input[@name='pass']").send_keys(Configue.FB_password)
        self.driver.find_element(By.XPATH, "//button[@name='login']").click()
        sleep(10)
        
        
        
    def scrape(self, keywords:list):
    
        for keyword in keywords:
            self.scrape_by_keyword(keyword)
            
            
    def scrape_by_keyword(self,keyword:str):
        self.driver.get("https://www.facebook.com/search/posts/?q={}".format(keyword))
        sleep(10)
        self.driver.execute_script("window.scrollTo(0, 200);")
        self.driver.find_element(By.XPATH, "//body").click()
        self.driver.find_element(By.XPATH, "//input[@aria-label='Recent Posts']").click()
        posts = self.driver.find_elements(By.XPATH,"//div[@role='feed']/div")