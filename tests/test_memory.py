from memory import Memory
from datetime import datetime
import os


class TestMemory:
    
    def test_create_memory(self):
        memory = Memory()
        assert memory is not None
        assert isinstance(memory, Memory)
        
    def test_save_timestamp(self):
        TestMemory.memory = Memory()
        TestMemory.memory .save_timestamp(datetime(2020,1,1), 'tests/test_memory_timestamp.txt')
        assert os.path.exists('tests/test_memory_timestamp.txt')
        with open('tests/test_memory_timestamp.txt','r') as fp:
            assert fp.read() == '2020-01-01 00:00:00'
            
    def test_load_timestamp(self):
        
        assert TestMemory.memory.load_timestamp('tests/test_memory_timestamp.txt') == datetime(2020,1,1)
        os.remove('tests/test_memory_timestamp.txt')
        
    def test_prepare_data_file(self):
        memory = Memory()
        memory._prepare_data_file('tests/test_memory_data.csv')
        with open('tests/test_memory_data.csv','r') as fp:
            assert fp.read() == 'date;la personne;la page (le compte);message;description;lien de media (image|video);les tags\n'
        os.remove('tests/test_memory_data.csv')
        
    def test_save_data(self):
        memory = Memory()
        memory.save_data('data', 'tests/test_memory_data.csv')
        with open('tests/test_memory_data.csv','r') as fp:
            lines = fp.readlines()
            assert len(lines) == 2
            assert lines[0] == 'date;la personne;la page (le compte);message;description;lien de media (image|video);les tags\n'
            assert lines[1] == 'data\n'
        os.remove('tests/test_memory_data.csv')
        
    def test_save_links(self):
        memory = Memory()
        memory.save_link('link1', 'tests/test_memory_links.txt')
        memory.save_link('link2', 'tests/test_memory_links.txt')
        with open('tests/test_memory_links.txt','r') as fp:
            lines = fp.readlines()
            assert len(lines) == 2
            assert lines[0] == 'link1\n'
            assert lines[1] == 'link2\n'
        
        
    def test_load_links(self):
        memory = Memory()
        memory.load_links('tests/test_memory_links.txt')
        with open('tests/test_memory_links.txt','r') as fp:
            lines = fp.readlines()
            assert len(lines) == 2
            assert lines[0] == 'link1\n'
            assert lines[1] == 'link2\n'
        os.remove('tests/test_memory_links.txt')
            
        