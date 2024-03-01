from selenium.webdriver import Chrome, ChromeOptions
from json import load
from os.path import exists
import traceback
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Driver:
    '''Run all functions through `driver.exe(func, *args)` to guarantee their success.\n
   !!! If you don't use cookies, sometimes you have to click 'continue as guest' before tiktok serves you posts!!! '''
    
    def __init__(self) -> None:
        self.driver = None
        self.last_url = 'https://tiktok.com/'
        self.username = ''
        self.make_new_driver()
        
    def make_new_driver(self):
        print("Launching new driver instance.")
        if self.driver is not None:
            self.driver.quit()
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-gpu')
        options.add_argument('enable-automation')
        self.driver = Chrome(options=options)
        self.driver.minimize_window()
        self.driver.get('https://tiktok.com/')
        if exists('cookies.json'):
            with open('cookies.json', 'r') as file:
                for cookie in load(file):
                    self.driver.add_cookie({
                        'name': cookie['name'],
                        'value': cookie['value']
                    })
        self.driver.get(self.last_url)
        
    def exe(self, func, *args):
        '''Relaunches the native driver if it runs into an OUT OF MEMORY webdriver error. A common enough occurence to warrant this.'''
        while True:
            try:
                return func(args)
            except Exception as e:
                traceback.print_exc()
                self.make_new_driver()
                
    def go_to_user(self, username: str) -> None:
        '''If no connection, will retry indefinitely.'''
        self.last_url = f'https://tiktok.com/@{username}'
        self.username = username
        while True:
            try:
                self.driver.get(self.last_url)
                break
            except WebDriverException:
                print(f'No internet while navigating to \'{username}\'. Trying again soon.')
                sleep(5)
                
    def does_current_user_exist(self) -> bool:
        try: 
            error_element = self.driver.find_element(By.CLASS_NAME, 'emuynwa1')
            return error_element.text != "Couldn't find this account"
        except NoSuchElementException:
            return True
        
    def get_recent_post_ids(self, timeout: int=5) -> list[str]:
        '''Only returns posts that tiktok serves you initially. Does not include posts you must scroll down for.'''
        try:
            #elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'eih2qak0')))
            sleep(3)
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            def filter_href(x:str):
                return x is not None and f'/@{self.username}/video/' in x
            hrefs = list(filter(filter_href, [element.get_attribute('href') for element in elements]))
            post_ids = [href.split('/')[-1] for href in hrefs]
            return post_ids
        except TimeoutException:
            print("Timeout exception for", self.driver.current_url)
            return []
        except StaleElementReferenceException:
            print("Stale element for", self.driver.current_url)
            return []
        except NoSuchElementException:
            print("No such element exception for", self.driver.current_url)
            return []
