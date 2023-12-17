## Usage
- Create a Virtual Environment (Preferably with Python 3.10): `python3.10 -m venv scrapper_env` <br>
- Activate the V ENV `source scrapper_env/bin/activate` <br>
- Install requirements `python -m pip install -r requirements`<br>

Please ensure Java (JRE) is installed on your system<br><br>
## Scraping Instructions
If you want to scrape from:<br>
- TIKTOK : Refer to the example in `tiktok_scrapper_job.py` . This script extracts information from the reels in the explore page of TikTok based on keywords.
- X : Insert your account information in `configue/configue.py`, then run the file `x_scrapper_job.py`,<br>There are two modes: 
    - Date Interval Scraping: Scrape data from a specified date range.
    - Real-Time Scraping: Track and scrape current data in real-time.<br>

The results will be found in `memory/data`<br>
Additionally, there is a simple example of data processing using PySpark in `preprocess_job.py`



 
