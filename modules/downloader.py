from queue import Queue
from threading import Thread
import pandas as pd
from downloaders.savetik import SavetikDownloader
from modules.path_generator import PathGenerator

def consumer(downloader):
    print("Download thread started.")
    downloaders = [
        SavetikDownloader()
    ]
    downloader_index = 0
    while True:
        post_id, directory = downloader.queue.get()
        path_generator = PathGenerator(directory)
        print(f'Download {post_id} to {directory}')
        downloaders[downloader_index].download_tiktok(f'https://tiktok.com/@/video/{post_id}', path_generator.filepath(post_id))
        downloader.df = downloader.df[downloader.df['Post Id'] != post_id]
        downloader.df.to_csv('data/download_queue.csv', index = False)
        print('Downloaded')
        downloader_index = (downloader_index + 1) % len(downloaders)
        
class Downloader:
    def __init__(self) -> None:
        self.queue = Queue()
        self.df = pd.read_csv('data/download_queue.csv')
        for post_id, directory in zip(self.df['Post Id'], self.df['Directory']):
            self.queue.put((post_id, directory))
        self.thread = Thread(target=consumer, args=[self])
        
    def enqueue(self, post_id: str, directory: str):
        if (len(self.df.loc[self.df['Post Id'] == post_id])>0):
            print(f'Can\'t enqueue {directory} {post_id}. Already in queue')
        else:
            self.queue.put((post_id, directory))
            self.df.loc[len(self.df)] = [post_id, directory]
            self.df.to_csv('data/download_queue.csv', index=False)
            print(f'Enqueued {post_id} in {directory}')