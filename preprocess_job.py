from processing import ProcessData

process = ProcessData()

files = {
    'x':'./memory/data/tweets_by_scraping.csv',
    'tiktok':'./memory/data/tiktok_by_scraping.csv',
    'output':'./memory/data/resultat.xlsx'
}

process.process(files)