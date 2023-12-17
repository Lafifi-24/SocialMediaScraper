import re
from time import sleep
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By

from memory import Memory


class X_Scrapper():
    
    
    def __init__(self, email:str, password:str, phone_number:str):
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self._start_scraping_envirenment()
        self.memory = Memory()
        
        
    def _start_scraping_envirenment(self):
        self.driver = webdriver.Edge()
        try:
            self.driver.get("https://twitter.com/i/flow/login")
            sleep(10)
            self.driver.find_element(By.XPATH, "//input[@autocomplete='username']").send_keys(self.email)
            self.driver.find_element(By.XPATH, "//span[*[text()='Next']]").click()
            sleep(5)
            try:# it appears when There was unusual login activity on your account
                self.driver.find_element(By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']").send_keys(self.phone_number)
                self.driver.find_element(By.XPATH, "//div[@data-testid='ocfEnterTextNextButton']").click()
                sleep(5)
            except:
                pass
            
            self.driver.find_element(By.XPATH, "//input[@autocomplete='current-password']").send_keys(self.password)
            self.driver.find_element(By.XPATH, "//span[*[text()='Log in']]").click()
            sleep(5)
            try:# to close the pop up if it appears (it suggest to activate two factor authentification)
                self.driver.find_element(By.XPATH, "//div[@aria-label='Close']").click()
            except:
                pass
        except:
            raise ValueError("Error : check your credentials or the stability of your network")
    
    def save_timestamp_of_last_scrapping(self,timestampe:datetime, keyword:str):
        path = './memory/timestamp/last_scrape_{}_tweets.txt'.format(keyword)       
        self.memory.save_timestamp( timestampe, path)
        
    def load_timestamp_of_last_scrapping(self, keyword:str):
        path = './memory/timestamp/last_scrape_{}_tweets.txt'.format(keyword)
        return self.memory.load_timestamp(path)    
    
    
    def save_data(self, data:dict, keyword:str):
        path = './memory/data/tweets_by_scraping.csv'
        data['description'] = data['description']+'|'+keyword+'|scraping'
        row = data['date']+'; '+data['la personne']+'; '+data['la page (le compte)']+'; '+data['message']+'; '+data['description']+'; '+data['lien de media (image ou video)']+'; '+data['les tags (Mots clés)']
        print(row)
        self.memory.save_data(row, path)
    
    
    
        
    def scrape(self, keywords:list, start:datetime=None, end:datetime=None):
        
        for keyword in keywords:
            super_break = 0
        
            if start is not None and end is not None:
                
                self.update_page("until%3A{}%20since%3A{}%20{}".format(end.strftime('%Y-%m-%d'), start.strftime('%Y-%m-%d'), keyword))
                limit_time = start
            else:
                currentTime = datetime.now()
                self.update_page(keyword)
                limit_time = self.load_timestamp_of_last_scrapping(keyword)
                
            
            time = None

            
            if limit_time is None:
                limit_time = currentTime + timedelta(hours = -2)
            else:
                limit_time = limit_time + timedelta(hours = -1.1)#to fix a decalage problem
            
            while True:
                n_time = self.scrape_tweets_in_current_screen(keyword, time)
                print('{}        {}'.format(n_time, time))
                if n_time is not None:
                    if limit_time > n_time:
                        break
                    
                    elif time is not None:
                        if n_time == time:
                            super_break += 1
                            if super_break > 10:
                                break
                        else:
                            super_break = 0
                            print('scraping more tweets')
                    time = n_time
            if start is None and end is None:
                self.save_timestamp_of_last_scrapping(currentTime, keyword)
        
        if start is None and end is None:# if we are scraping in real time
            sleep(60*60)
            self.scrape(keywords)
                
            
        
    def update_page(self, keyword:str):
        self.scroll_base = 0
        self.scroll_new = 0
        self.driver.get('https://twitter.com/search?q={}&f=live'.format(keyword))
        sleep(5)
        
    def scrape_tweets_in_current_screen( self,keyword:str,timestampe_of_last_tweet_from_previous_scrapping:datetime = None):
        tweets = self.driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        format = '%Y-%m-%dT%H:%M:%S.%fZ'
        timestamp_of_last_tweet = timestampe_of_last_tweet_from_previous_scrapping
        for i,tweet in enumerate(tweets):
            
            try :
                time = tweet.find_element(By.XPATH,".//time").get_attribute('datetime')
                user = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']").find_element(By.XPATH, ".//a")
                profile_link = user.get_attribute('href')
                username = user.text
                try:# if we have image
                    tweet_image = tweet.find_element(By.XPATH, ".//img[@alt='Image']")
                    tweet_image_link = tweet_image.get_attribute('src')
                except:
                    tweet_image_link = None
                
                try:# if we have video
                    tweet_video = tweet.find_element(By.XPATH, ".//video")
                    tweet_video_link = tweet_video.get_attribute('src')
                except:
                    tweet_video_link = None
                
                
                
                self.scroll_new += tweet.size['height']
                
                TweetText = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                    
                hashtags = re.findall(r'#\w+', TweetText)
                mentions = re.findall(r'@\w+', TweetText)
                data = {
                    'date':time , 
                    'la personne':username, 
                    'la page (le compte)': profile_link,  
                    'message':TweetText.replace("\n", " ").replace(";", " ") ,  
                    'description': 'tweet', 
                    'lien de media (image ou video)': str(tweet_image_link)+'|'+str(tweet_video_link),
                    'les tags (Mots clés)': ' '.join(hashtags)+' '+' '.join(mentions),
                }
                
                timestamp_of_last_tweet = datetime.strptime(time, format)
                if timestampe_of_last_tweet_from_previous_scrapping is not None:
                    if timestamp_of_last_tweet < timestampe_of_last_tweet_from_previous_scrapping:
                        self.save_data(data, keyword)
                else:
                    self.save_data(data, keyword)
                    
            except:
                print('enable to scrape tweet')

            
        self.driver.execute_script("window.scrollTo({}, {});".format(self.scroll_base, self.scroll_new))
        sleep(10) 
        self.scroll_base = self.scroll_new
        
        return timestamp_of_last_tweet
        

