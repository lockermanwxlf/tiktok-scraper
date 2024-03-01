import pandas as pd
import os
from path import OUTPUT_DIR
from modules.driver import Driver
from time import sleep
from modules.path_generator import PathGenerator
from modules.downloader import Downloader

def file_not_present(dir, prefix):
    os.makedirs(dir, exist_ok=True)
    for s in os.listdir(dir):
        if prefix in os.path.splitext(s)[0] and os.path.isfile(os.path.join(dir, s)):
            return False

    return True 


def ensure_files():
    for path, columns in {
        'data/download_queue.csv': ['Post Id', 'Directory'],
        'data/history.csv': ['Profile Id', 'Post Id'],
        'data/profiles.csv': ['Username', 'Directory', 'Id']
    }.items():
        if not os.path.exists(path):
            pd.DataFrame(columns = columns).to_csv(path, index=False)
    

def main():
    ensure_files()
    driver = Driver()
    downloader = Downloader()
    while True:
        df = pd.read_csv('data/profiles.csv')
        for directory, username, id in zip(df['Directory'], df['Username'], df['Id']):
            pathgen = PathGenerator(directory)
            
            driver.go_to_user(username)
            for id in filter(lambda id: file_not_present(pathgen.output_dir, pathgen.filename(id)), driver.get_recent_post_ids()):
                downloader.enqueue(id, directory)
            sleep(3)
        
    
if __name__ == '__main__':
    main()