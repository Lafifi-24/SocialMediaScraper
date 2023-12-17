from datetime import datetime
import os

import pytest

from navigator import X_Scrapper
from configue import Configue



class TestXScrapper():
    

    def test_create_x_scrapper_with_success(self):
        TestXScrapper.x_scraper = X_Scrapper(Configue.X_email, Configue.X_password, Configue.X_phone_number)
        assert TestXScrapper.x_scraper is not None
        assert isinstance(TestXScrapper.x_scraper, X_Scrapper)
        TestXScrapper.x_scraper.driver.close()
        
        
        
    def test_create_x_scrapper_with_fail(self):
        with pytest.raises(Exception) as e_info:
            x_scraper = X_Scrapper('hamzalafifi@gmail.com','AZER6789','0611111111')
            assert e_info.value == "Error : check your credentials"
            x_scraper.driver.close()
            
    def test_save_timestamp_of_last_scrapping(self):
        TestXScrapper.x_scraper.save_timestamp_of_last_scrapping(datetime.now(), 'testtest')
        assert os.path.exists('./memory/timestamp/last_scrape_testtest_tweets.txt')

    def test_load_timestamp_of_last_scrapping(self):
        assert isinstance(TestXScrapper.x_scraper.load_timestamp_of_last_scrapping('testtest'),datetime)
        os.remove('./memory/timestamp/last_scrape_testtest_tweets.txt')
        
            
            