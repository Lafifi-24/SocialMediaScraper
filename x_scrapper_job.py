from navigator import X_Scrapper
from configue import Configue
from time import sleep
from datetime import datetime

def run(start:datetime= None, end:datetime=None):
    navigator = X_Scrapper(Configue.X_email, Configue.X_password, Configue.X_phone_number)
    

    navigator.scrape(['maroc','المغرب','morocco'], start, end)

    navigator.driver.close()
    print('shut down')
    if start is None and end is None:
        sleep(1000)
        run()
start = datetime(2023, 12, 7)
end = datetime(2023, 12, 8)
# run(start, end)
run()
    