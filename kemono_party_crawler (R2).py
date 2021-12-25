import requests
import os
import time
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from datetime import datetime
from selenium.webdriver.common.keys import Keys

import savemysql


def get_card(painter_name):

    username = input('Enter you username: ')

    password = input('Enter you password: ')

    ChromeOptions = Options()

    ChromeOptions.add_argument('--headless')

    prefs = {"profile.managed_default_content_settings.images": 2}

    ChromeOptions.add_experimental_option("prefs", prefs)

    # time.sleep is choose on you.

    driver = webdriver.Chrome(chrome_options = ChromeOptions)

    time.sleep(5)

    driver.get("https://kemono.party/account/login")

    time.sleep(10)

    driver.find_element_by_name("username").send_keys(username)

    time.sleep(3)

    driver.find_element_by_name("password").send_keys(password)

    time.sleep(3)

    driver.find_element_by_xpath("//*[@type='submit']").submit()
    
    time.sleep(10)

    driver.get("https://kemono.party/artists?o=0")
    
    time.sleep(10)

    driver.find_element_by_id("q").send_keys(painter_name, Keys.ENTER)

    time.sleep(5)

    painter_url = driver.find_element_by_link_text(painter_name).get_attribute('href');
    
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]

    cookiestr = ";".join(item for item in cookie)
    
    driver.quit()

    return painter_url, cookiestr



def download_chunk(url, path):
    with requests.get(url, headers = get_headers(), stream = True) as r:
        r.raise_for_status()
        with open(path, "wb") as file:
            for chunk in r.iter_content(chunk_size = 8192):
                if chunk:
                    file.write(chunk)


def get_html(url):
    response = requests.get(url, headers = get_headers(), allow_redirects=True)
    return response.text


def get_headers():
    ua = UserAgent()
    headers = {'user-agent': ua.random, 'cookie': cookie}
    return headers


def get_post(url, next_page):

    posts = []

    recent_update_day = savemysql.check_day()

    if next_page == 'none':

        page_html = get_html(url)

        page_soup = BeautifulSoup(page_html, 'html.parser')

        cards = page_soup.find_all("article")

        for card in cards:

            parent = card.find('header', {"class", "post-card__header"})

            title = parent.find('a').getText().replace("\n", " ").strip()

            link = "https://kemono.party" + parent.find('a')["href"]

            try:

                post_time = card.find('time', {"class": "timestamp"}).getText().replace("\n", " ").strip()

            except:

                post_time = str(datetime.now()).split(" ")[0]

            day = post_time.split(" ")[0]

            if day > recent_update_day:

                posts.append({'title': title, 'post': link, 'img': [], 'video': [], 'day': day, 'name': painter_name})

            else:
                break

    while not next_page == 'none':

        page_html = get_html(url)

        page_soup = BeautifulSoup(page_html, 'html.parser')

        cards = page_soup.find_all("article")

        for card in cards:

            parent = card.find('header',{"class": "post-card__header"})

            title = parent.find('a').getText()

            link = "https://kemono.party" + parent.find('a')["href"]

            post_time = card.find('time', {"class": "timestamp"}).getText()

            day = post_time.split(" ")[1]

            if day > recent_update_day:

                posts.append({'title': title, 'post': link, 'img': [], 'video': [], 'day': day, 'name': painter_name})

            else:
                break

        try:
            next_page = "https://kemono.party" + page_soup.find("a", {"title": "Next page"})["href"]

        except:
            next_page = 'none'

        url = next_page

        time.sleep(3)

    return posts


def get_img(posts):

    for post in posts:

        post_html = get_html(post['post'])

        page_soup = BeautifulSoup(post_html, 'html.parser')

        images = page_soup.find_all("div", {"class": "post__thumbnail"})
        
        for image in images:

            pic = image.find('a', {'class': 'fileThumb'})['href']

            post['img'].append(pic)

        videos = page_soup.find_all("a", {"class": "post__attachment-link"})

        for video in videos:

            post['video'].append(video['href'])

        time.sleep(3)

    return posts



def Download_post(painter_dict):

    dirpath = r'.\{0}'.format(painter_name)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    iter = 0

    for data in painter_dict:

        for img in data["img"]:

            imgurl = "https://data3.kemono.party" + img

            imgext = img.split('.')[-1]

            title = data['title'].replace(':', ' ').replace('/', ' ')
                
            img_file_path = r'.\{0}\{1}.{2}'.format(painter_name, (title + " {0}".format(iter)), imgext)
                
            download_chunk(imgurl, img_file_path)

            print('Image: {0} \n  Download Success'.format(title))

            iter = iter + 1

        for video in data["video"]:

            videourl = "https://data3.kemono.party" + video

            videoext = video.split('.')[-1]

            title = data['title'].replace(':', ' ').replace('/', ' ')

            video_file_path = r'.\{0}\{1}.{2}'.format(painter_name, (title + " {0}".format(iter)), videoext)

            download_chunk(videourl, video_file_path)

            print('Video: {0} \n Download Success'.format(title))

            iter = iter + 1
        
        iter = 0


def main(url):

    html = get_html(url)

    soup = BeautifulSoup(html, "html.parser")

    try :

        next_page = soup.find("a", {"title": "Next page"})["href"]

    except:

        next_page = 'none'
    
    print('get next page success')

    posts = get_post(url, next_page)

    print('get post success')

    painter_dict = get_img(posts)
    
    print('get image success')

    '''
    The following functions are for your choice.
    '''

    Download_post(painter_dict)

    print('Download all post image & video success')

    savemysql.sql_saved(painter_dict)

    print('SQL save success')
    

if __name__ == '__main__':

    start = time.time()

    painter_name = input('Artist name: ')

    url, cookie = get_card(painter_name)

    main(url)

    print('All Steps Success !!!! ╮(╯  > ╰ )╭')

    end = time.time()

    total_time = end - start

    hour = total_time // 3600

    min = (total_time - 3600 * hour) // 60

    sec = total_time - 3600 * hour - 60 * min

    print(f'Totel spend time:{int(hour)}h {int(min)}m {int(sec)}s')
