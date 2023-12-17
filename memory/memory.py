from datetime import datetime
import os

class Memory:
    def __init__(self):
        self.timestamp_format = '%Y-%m-%d %H:%M:%S'
    
    def save_timestamp(self, time:datetime, path:str):
        with open(path,'w') as fp:
            fp.write(time.strftime(self.timestamp_format))
            
    def load_timestamp(self, path:str):
        if os.path.exists(path):
            with open(path,'r') as fp:
                return datetime.strptime(fp.read(), self.timestamp_format)
        else:
            return None
    
    def _prepare_data_file(self, path:str):
        with open(path,'w') as fp:
            fp.write('date;la personne;la page (le compte);message;description;lien de media (image|video);les tags\n')
    
    def save_data(self, data:str, path:str):
        if os.path.exists(path):
            with open(path,'a') as fp:
                fp.write(data+'\n')
        else:
            self._prepare_data_file(path)
            self.save_data(data, path)
            
    def save_link(self, link:list, path:str):
        if os.path.exists(path):
            with open(path,'a') as fp:
                
                fp.write(link+'\n')
        else:
            with open(path,'w') as fp:
                
                fp.write(link+'\n')
                    
    def load_links(self, path:str):
        if os.path.exists(path):
            with open(path,'r') as fp:
                return fp.readlines()
        else:
            return []