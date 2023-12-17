from navigator import TiktokScrapper
from time import sleep

def run():
    navigator = TiktokScrapper()
    navigator.scrape(['maroc','المغرب','morocco'], 1000)#scrape  1000 reels if possible every time
    navigator.driver.close()
    print('shut down')
    sleep(3*60*60)
    run()#to scrape every 3 hours

run()
    