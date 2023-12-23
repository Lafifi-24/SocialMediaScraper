from pyspark.sql.functions import to_timestamp, format_string
from pyspark.sql import SparkSession



class ProcessTikTokData:
    def __init__(self, spark:SparkSession):
        self.spark = spark
        
    def fix_media_link(self, df):
        return df.withColumn('lien de media (image|video)',format_string('None|%s',df['lien de media (image|video)']))
    
    def process(self, df):
        # list of data processing functions
        df = self.fix_media_link(df)
        return df
        
class ProcessXData:
    def __init__(self, spark:SparkSession):
        self.spark = spark
        
    def fix_date_format(self, df):
        return df.withColumn('date',to_timestamp(df.date))
    
    def process(self, df):
        # list of data processing functions
        df = self.fix_date_format(df)
        return df

class ProcessData:
    def __init__(self):
        self.spark = SparkSession.builder.appName("Processer").getOrCreate()
        self.process_tiktok = ProcessTikTokData(self.spark)
        self.process_x = ProcessXData(self.spark)


    
    def process(self, files:dict):
        if files['tiktok'] is not  None:
            df = self.spark.read.csv(files['tiktok'], header=True,sep=';')
            tiktok = self.process_tiktok.process(df)
        if files['x'] is not None:
            df = self.spark.read.csv(files['x'], header=True,sep=';')
            x = self.process_x.process(df)
            
            
        
        if tiktok is not None and x is not None:
            data = x.union(tiktok).toPandas()
        elif tiktok is None and x is not None:
            data = x.toPandas()
        elif x is None and tiktok is not None:
            data = tiktok.toPandas()
        self.data = data
        self.data.drop_duplicates(inplace=True)
        
    def save(self, files:dict):
        self.data.to_excel(files['output'],sheet_name='data', index=False)
        