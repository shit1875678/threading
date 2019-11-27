import requests
from tqdm import tqdm
import queue
from threading import Thread
from bs4 import BeautifulSoup
import time


def get_movie_dtail():
    while Que.qsize() > 1:
        movie_url = Que.get()
        res = requests.get(movie_url)
        soup = BeautifulSoup(res.text, 'lxml')
        movie_name = soup.find('div', 'movie_intro_info_r').find('h1').text
        f = open('movie_name.txt', 'a',encoding='utf-8')
        f.write('\n' + movie_name)
        f.close()
        print(movie_name)
    time.sleep(1)


def get_page_num(main_url):
    res = requests.get(main_url)
    soup = BeautifulSoup(res.text, 'lxml')
    Max_page = soup.find('div', 'page_numbox').find_all('li')[-3].text
    return Max_page




def get_all_movie_url(Max_page):
    all_movie_url = []
    for page_num in range(int(Max_page)):
        page_num = page_num + 1
        url = 'https://movies.yahoo.com.tw/movie_intheaters.html?page=' + str(page_num)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        movie_urls = soup.find_all('div','release_foto')
        for movie_url in movie_urls:
            movie_url = movie_url.find('a')['href']
            all_movie_url.append(movie_url)
    return all_movie_url





if __name__ == '__main__':
    Main_url = 'https://movies.yahoo.com.tw/movie_intheaters.html?page=1'
    Max_page = get_page_num(Main_url)
    a_list = get_all_movie_url(Max_page)
    Que= queue.Queue()
    for item in a_list:
        Que.put(item)
    get_dtail_team = []
    for ii in range(30):
        get_dtail = Thread(target=get_movie_dtail)
        get_dtail.start()
        get_dtail_team.append(get_dtail)
    for get_dtail in tqdm(get_dtail_team):
        get_dtail.join()
