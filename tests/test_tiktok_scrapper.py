from navigator import TiktokScrapper
from selenium import webdriver
import os


class TestTiktokScrapper:
    def test_create_tiktok_scrapper(self):
        tiktok_scrapper = TiktokScrapper()
        assert tiktok_scrapper is not None
        assert isinstance(tiktok_scrapper, TiktokScrapper)
        assert isinstance(tiktok_scrapper.driver, webdriver.Edge)
        tiktok_scrapper.driver.close()
        

        
    def test_save_data(self):
        tiktok_scrapper = TiktokScrapper()
        data = {
                'date':'date' , 
                'la personne':'author_name', 
                'la page (le compte)': 'author_profile',  
                'message':'reel_text',  
                'description': 'tiktok', 
                'lien de media (image ou video)': 'video_url',
                'les tags (Mots clés)': 'hashtags'
            }
        tiktok_scrapper.save_data_row(data, 'test')
        data['description'] = data['description']+'|test|scraping'
        row = data['date']+'; '+data['la personne']+'; '+data['la page (le compte)']+'; '+data['message']+'; '+data['description']+'; '+data['lien de media (image ou video)']+'; '+data['les tags (Mots clés)']
        
        with open('./memory/data/tiktok_by_scraping.csv','r') as fp:
            lines = fp.readlines()
            assert len(lines) == 2
            assert lines[0] == 'date;la personne;la page (le compte);message;description;lien de media (image|video);les tags\n'
 
        os.remove("./memory/data/tiktok_by_scraping.csv")