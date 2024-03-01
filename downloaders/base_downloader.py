from requests import Session
from requests.exceptions import ChunkedEncodingError
import os
from fake_useragent import UserAgent

class BaseDownloader:
    def __init__(self):
        self.session = Session()
    
    def get_current_size(file_path: str):
        if not os.path.exists(file_path):
            return 0
        else:
            return os.path.getsize(file_path)
    
    def download_url_to_file(self, url: str, file_path: str):
        ua = UserAgent()
        current_size = BaseDownloader.get_current_size(file_path)
        headers = {
            'User-Agent': ua.random
        }
        content_length = int(self.session.get(url, stream=True, headers=headers).headers['Content-Length'])
        print("Current size", current_size)
        print("Content length", content_length)
        while (content_length != current_size):
            headers['User-Agent'] = ua.random
            headers['Range'] = f'bytes={current_size}-{content_length}'
            with self.session.get(url, stream=True, headers=headers) as response:
                print("Ok", response.ok)
                if response.ok:
                    with open(file_path, 'ab+') as file:
                        try:
                            for block in response.iter_content(1024):
                                if not block:
                                    break
                                file.write(block)
                        except ChunkedEncodingError as e:
                            print("CHUNKEDENCODINGERROR")
                        #shutil.copyfileobj(response.raw, file, length=16*1024*1024)
                current_size = BaseDownloader.get_current_size(file_path)
        return True
    
    def download_tiktok(self, tiktok_url: str, file_path_no_extension: str) -> bool:
        print("Downloaded", tiktok_url)
        return True