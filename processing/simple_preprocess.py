from pyspark.sql.functions import to_timestamp, format_string
from pyspark.sql import SparkSession





class PreProcess:
    def __init__(self):
        self.spark = SparkSession.builder.appName("CSV to Excel").getOrCreate()

    
    def preprocess_tiktok(self, path:str):
        df = self.spark.read.csv(path, header=True,sep=';')
        df = df.withColumn('lien de media (image|video)',format_string('None|%s',df['lien de media (image|video)']))
        return df
    
    def preprocess_x(self,path:str):
        df = self.spark.read.csv(path, header=True,sep=';')
        df = df.withColumn('date',to_timestamp(df.date))
        return df
    
    def preprocess(self, files:dict):
        x = self.preprocess_x(files['x'])
        tiktok = self.preprocess_tiktok(files['tiktok'])
        data = x.union(tiktok).toPandas()
        data.drop_duplicates(inplace=True)
        data.to_excel(files['output'],sheet_name='data', index=False)
        