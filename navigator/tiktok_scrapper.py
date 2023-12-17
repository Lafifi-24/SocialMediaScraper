from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, timedelta

import re

from memory import Memory


class TiktokScrapper:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.memory = Memory()
        
        
    def prepare_the_envirenment(self, keyword:str):
        try:
            self.driver.get("https://www.tiktok.com/search?q={}".format(keyword))
            sleep(10)
            
        except:
            raise ValueError("Error: Can't open tiktok.com")
    def get_history(self,links):
        history=[]
        for link in links:
            history.append(link.split('/')[-1])
        return history
    def get_reels_link(self, reels:list):
        history = self.get_history(self.memory.load_links('./memory/data/tiktok_reels_links.txt'))
        result = []
        for i, reel in enumerate(reels):
            try:
                link= reel.find_element(By.XPATH,".//div[contains(@class, 'DivWrapper')]").find_element(By.XPATH,".//a").get_attribute("href")
                if str(link).split('/')[-1] not in history:
                    result.append(link)
                
                    
            except:
                print("Can't get the link")
        
        return result
    
    def scrape(self,keywords:list,reels_number:int =500):
        for keyword in keywords:
            reels = self.scrape_by_keyword(reels_number, keyword)
            self.get_reels_description(reels,keyword)
            
        sleep(6*60*60)
        self.scrape(keywords, reels_number)
            
            
    def scrape_by_keyword(self, reels_number:int, keyword:str):
        super_break = 0
        self.prepare_the_envirenment(keyword)
        new_reels = []
        while len(new_reels) < reels_number:
            temp_break = len(new_reels)
            try:
                if self.driver.find_element(By.XPATH,"//div[contains(@class, 'DivNoMoreResultsContainer')]"):
                    print("limit the page")
                    break
                
            except:
                pass
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(10)
                new_reels = self.driver.find_elements(By.XPATH,"//div[contains(@class, 'DivItemContainerForSearch')]")
            except:
                try:
                    print("Can't scroll down")
                    button = self.driver.find_element(By.XPATH,"//div[contains(@class, 'DivErrorContainer')]")
                    button.find_element(By.XPATH,".//button").click()
                except:
                    print("unexpected error")
                    
            if  temp_break == len(new_reels):
                super_break += 1
                print("can't scroll down")
                if super_break >10:
                    break
        
        reels = self.get_reels_link(new_reels)

        return reels
        
    def get_reel_description(self, reel_url:str,keyword:str):

        try:
            self.driver.get(reel_url)
            video_container = self.driver.find_element(By.XPATH,"//div[contains(@class, 'DivVideoContainer')]")
            self.driver.execute_script("window.scrollTo(0, 200);")
            video_url = video_container.find_element(By.XPATH,".//video").get_attribute("src")
            description_container = self.driver.find_element(By.XPATH,"//div[contains(@class, 'DivDescriptionContentWrapper')]")
            author = description_container.find_element(By.XPATH,".//div[contains(@class, 'DivAuthorContainer')]")
            author_name = author.find_element(By.XPATH,".//span[contains(@class,'SpanUniqueId')]").text
            date = author.find_element(By.XPATH,".//span[contains(@class,'SpanOtherInfos')]").find_elements(By.XPATH,".//span")[-1].text
            reel_text = description_container.find_element(By.XPATH,".//h1[contains(@class,'H1Container')]").text
            hashtags = re.findall(r'#\w+', reel_text)
            author_profile = author.find_element(By.XPATH,".//a").get_attribute("href")
            
            data = {
                    'date':self.get_date(date).strftime("%Y-%m-%d %H:%M:%S") , 
                    'la personne':author_name, 
                    'la page (le compte)': author_profile,  
                    'message':reel_text.replace("\n", " ").replace(";", " "),  
                    'description': 'tiktok', 
                    'lien de media (image ou video)': str(video_url),
                    'les tags (Mots clés)': ' '.join(hashtags)
                }
            self.memory.save_link(reel_url, './memory/data/tiktok_reels_links.txt')
            print(data)
            self.save_data_row(data, keyword)
        except:
            print("Can't get the description")
        
        
    def save_data_row(self, data:dict, keyword:str):
        path = './memory/data/tiktok_by_scraping.csv'
        data['description'] = data['description']+'|'+keyword+'|scraping'
        row = data['date']+'; '+data['la personne']+'; '+data['la page (le compte)']+'; '+data['message']+'; '+data['description']+'; '+data['lien de media (image ou video)']+'; '+data['les tags (Mots clés)']
        print(row)
        self.memory.save_data(row, path)
        
    def get_reels_description(self,reels:list, keyword:str):
        for reel in reels:
            if reel is not None:
                self.get_reel_description(reel, keyword)
                
    def get_date(self, date:str):
        date_temp = date.split('-')
        if len(date_temp) == 1:
            day=re.findall(r'\d+d', date)
            hours=re.findall(r'\d+h', date)
            if len(day) != 0:
                return datetime.now()-timedelta(days=int(re.findall(r'\d+', date)[0]))
            else:
                return datetime.now()-timedelta(hours=int(re.findall(r'\d+', date)[0]))
        elif len(date_temp) == 2:
            return datetime.strptime('{}-{}'.format(datetime.now().year,date), '%Y-%m-%d')
        elif len(date_temp) == 3:
            try : 
                temp = datetime.strptime(date, '%Y-%m-%d')
            except:
                temp = datetime.strptime(date, '%y-%m-%d')
            return temp
        return None