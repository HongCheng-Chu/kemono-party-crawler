import requests
import urllib.request
import os
import time
import json
import random
import re
from hashlib import md5
from bs4 import BeautifulSoup
from http import cookiejar


"""
# if selenium is available, you can use the following function to take the artist ID, and delete the Painter_url which need to input.

# I did not test this function, because my googledriver can not work, I think this has a few problem.

def get_id(Painter_name):

    ChromeOptions = Options()

    ChromeOptions.add_argument('--headless')

    # time.sleep is choose on you.

    driver = webdriver.Chrome(chrome_options = ChromeOptions)
    
    time.sleep(3)

    driver.get("https://kemono.party/artists")
    
    time.sleep(3)

    driver.find_element_by_xpath("//div[input/@name='q']").send_keys(Painter)

    time.sleep(3)

    Painter_id = driver.find_element_by_xpath('//a[text()={0}]').format(Painter).get_attribute('href')
    
    Painter_id = "https://kemono.party" + Painter_id

    driver.quit()

    return Painter_id
"""


def download_chunk(url, path):
    with requests.get(url, headers = headers, stream = True) as r:
        r.raise_for_status()
        with open(path, "wb") as file:
            for chunk in r.iter_content(chunk_size = 8192):
                if chunk:
                    file.write(chunk)


def get_html(url):
    response = requests.get(url, headers = headers, allow_redirects=True)
    return response.text # text return Unicode data -> get text


def get_post(url, next_page):

    post_links = []

    if next_page == 'none':

        page_html = get_html(url)

        page_soup = BeautifulSoup(page_html, 'html.parser')

        posts = page_soup.find_all("article")

        for post in posts:
            post_links.append("https://kemono.party" + post.find('a')["href"])
    
    time.sleep(5)

    while not next_page == 'none':

        page_html = get_html(url)

        page_soup = BeautifulSoup(page_html, 'html.parser')

        posts = page_soup.find_all("article")

        for post in posts:
            post_links.append("https://kemono.party" + post.find('a')["href"])

        try:
            next_page = "https://kemono.party" + page_soup.find("a", {"title": "Next page"})["href"]

        except:
            next_page = 'none'

        url = next_page

        time.sleep(5)

    return post_links


def Download_post(urls):

    dirpath = r'.\{0}'.format(Painter_name)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    
    iter = 1

    for i in range(len(urls)):

        post_html = get_html(urls[i])

        page_soup = BeautifulSoup(post_html, 'html.parser')

        img_url = page_soup.find_all("a", {"class" : "fileThumb"})

        if not img_url == []:
            
            for img in img_url:

                # data1,2,3 in URL is floating words, you can use any one to get image, video or etc. 
                # Data1,2,3 is high quality, thumb is low quality
                # If data3 download too slow, change to data1 or data2

                url = "https://data3.kemono.party" + img["href"]

                tmp = url

                urlext = tmp.split('.')[-1]
                
                file_path = r'.\{0}\{1}.{2}'.format(Painter_name, md5(url.encode('utf8')).hexdigest(), urlext)
                

                download_chunk(url, file_path)

                print('Img: {0} \n URL: {1} \n  Download Success'.format(iter, url))

                iter = iter + 1

        time.sleep(5)     
        
        mp4_url = page_soup.find_all("a", {"class" : "post__attachment-link"})
        
        if not mp4_url == []:
            
            for mp4 in mp4_url:

                url = "https://data3.kemono.party" + mp4["href"]

                tmp = url

                urlext = tmp.split('.')[-1]
                
                if not ((urlext == 'mp4') or (urlext == 'zip')):
                    continue

                file_path = r'.\{0}\{1}.{2}'.format(Painter_name, md5(url.encode('utf8')).hexdigest(), urlext)

                download_chunk(url, file_path)

                print('Video: {0} \n URL: {1} \n  Download Success'.format(iter, url))

                iter = iter + 1

        time.sleep(5)


def main(Painter_url):

    html = get_html(Painter_url)

    soup = BeautifulSoup(html, "html.parser")

    try :
        next_page = soup.find("a", {"title": "Next page"})["href"]
    except:
        next_page = 'none'
    
    print('get next page success')

    urls = get_post(Painter_url, next_page)

    print('get post success')

    Download_post(urls)

    print('Download all post image & video success')


"""
kemono.party website need cookie to do the web crawler.

Please add the cookie in headers.

Reminder: Login the member account may reduce the risk of banned. 
"""

headers = {
    'cookie': 'Please add cookie in here and delete these words'
,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
}

Painter_name = input('Enter a artist name')
Painter_url = input('Enter a artist URL with the post page') # or use get_id(Painter_name)

start = time.time()

main(Painter_url)

print(' All Steps Success !!!! ???(???  _ ??? )???')

end = time.time()

total_time = end - start
hour = total_time // 3600
min = (total_time - 3600 * hour) // 60
sec = total_time - 3600 * hour - 60 * min
print(f'Totel spend time:{int(hour)}h {int(min)}m {int(sec)}s')
