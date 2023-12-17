from processing import PreProcess

process = PreProcess()

files = {
    'x':'./memory/data/tweets_by_scraping.csv',
    'tiktok':'./memory/data/tiktok_by_scraping.csv',
    'output':'./memory/data/resultat.xlsx'
}

process.preprocess(files)