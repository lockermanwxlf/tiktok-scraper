# READ DISCLAIMER BEFORE USE!!!!!!!!!!!!!!!!
Disclaimer: Neither this project nor its Contributors are affiliated with ByteDance, TikTok, nor any of their services. It is your responsibility as a user of this program to obtain permission or authorization from copyright holders AND content creators before using, downloading, or reproducing material or content protected under copyright. Failing to do so is a violation of intellectual property rights.

# tiktok-scraper

Download posts from multiple TikTok profiles.

Selenium based
 
# Get Started

Read 'important' after doing this. Run this command in your terminal.
```
git clone https://github.com/lockermanwxlf/tiktok-scraper.git && \
cd tiktok-scraper && \
pip install -r requirements.txt
```
# Important
Create a file named path.py and declare `OUTPUT_DIR = "desired output directory"`. I am too lazy to make this an optional txt or json file.

If you have an account on TikTok, you can place a json file 'cookies.json' in the base directory. This will not let you download private posts, but it will help against some of TikTok's anti bot stuff.

Run main.py and edit data/profiles.csv.

## data/profiles.csv
Username: username of profile you want to download posts from

Directory: files will be downloaded to `f'{OUTPUT_DIR}/{Directory}'`. If set to nan, files will be downloaded to `f'{OUTPUT_DIR}`.

Id: Arbitrary unique id for the profile in the csv. For now has no purpose, but in the future, the profile_id will be used to track the post_id of the posts you download from them so that if they ever change their username, it automatically finds their new username (it will only work when their profile is public).

