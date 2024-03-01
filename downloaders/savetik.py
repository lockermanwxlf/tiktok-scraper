import json
import bs4
import os
from time import sleep
from downloaders.base_downloader import BaseDownloader

class SavetikDownloader(BaseDownloader):
    def _get_download_info(self, tiktok_url: str) -> tuple[str, list[str]] | None:
        request_url = 'https://tiksave.io/api/ajaxSearch'
        payload = "q={}&lang={}".format(tiktok_url, 'en')
        headers = {
            "authority": "tiksave.io",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://tiksave.io",
            "referer": "https://tiksave.io/en",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        response = self.session.post(url=request_url, data=payload, headers=headers)
        try:
            download_page_html = json.loads(response.text)['data']
        except KeyError:
            return None
        download_page_soup = bs4.BeautifulSoup(download_page_html)

        # Check for video download button.
        buttons = download_page_soup.find_all('a', attrs={'class': 'tik-button-dl button dl-success'})
        for button in buttons:
            if "Download MP4 HD" in button.text:
                return ('.mp4', [button.get('href')])
            
        # No video found, get all image download buttons.
        buttons = download_page_soup.find_all('a', attrs={'class': 'btn-premium'})
        if len(buttons) > 0:
            return ('.jpg', [button.get('href') for button in buttons])
        else:
            return None

    def download_tiktok(self, tiktok_url: str, file_path_no_extension: str):
        download_info = self._get_download_info(tiktok_url)
        if download_info is None:
            return
        if download_info[0] == '.mp4':
            self.download_url_to_file(download_info[1][0], file_path_no_extension + download_info[0])
        else:
            for image_number, download_url in enumerate(download_info[1], 1):
                file_path = f'{file_path_no_extension} {str(image_number)}{download_info[0]}'
                self.download_url_to_file(download_url, file_path)
                sleep(3)
        return super().download_tiktok(tiktok_url, file_path_no_extension)