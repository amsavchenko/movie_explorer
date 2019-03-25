from gensim.models.fasttext import FastText
from operator import itemgetter
import numpy as np
import os
from nltk.stem import WordNetLemmatizer
import string
from imdb import IMDb

from selenium.webdriver import Chrome 
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from multiprocessing import Pool
from functools import partial

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

lemmatizer = WordNetLemmatizer()
exclude = set(string.punctuation)
imdb = IMDb()
#model = FastText.load(os.path.expanduser('~/Documents/atom/imdb_model'))
model = FastText.load(os.path.expanduser('~/PycharmProjects/movie_explorer/Anton/imdb_model'))


string = ''
f = open(os.path.expanduser('~/PycharmProjects/movie_explorer/Anton/inew_better_descriptions.txt'), 'r')
string += f.read()
f.close()

descr = string.split('\n')
name_list = []
link_list = []
stop_list = ['kkk', 'wcw', 'uwwf', '4x4', 'tjs', 'são', 'rós', 'vfw', 'léa']


descr = [x for x in descr if x[:x.find('%$')+3:x.find('@@@')] != '']

descr_vectors = np.load(os.path.expanduser('~/PycharmProjects/movie_explorer/Anton/ivectors.npy'))
calculated_vectors = np.load(os.path.expanduser('~/PycharmProjects/movie_explorer/Anton/plot_vectors.npy'))


for i in descr:
    name_list.append(i[:i.find('%$')])
for i in descr:
    link_list.append(i[i.find('@@@')+3:])

for i in range(len(descr)):
    descr[i] = descr[i][descr[i].find('%$')+3:descr[i].find('@@@')]

id_list = [i[i.find('/tt')+3:-1] for i in link_list][:1530]


def return_id_from_title(title):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    #options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome"
    
    chrome_driver_binary = "/usr/local/bin/chromedriver"
    #chrome_driver_binary = "D:\mail-python\PrPythonAtom\homeworks\project\chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    # driver = Chrome(executable_path = 'C:\webdrivers\chromedriver')
    driver.get('https://www.imdb.com/')

    choose = driver.find_element_by_xpath('//*[@id="quicksearch"]')
    choose.click()
    titles = driver.find_element_by_xpath('//*[@id="quicksearch"]/option[2]')
    titles.click()
    search_form = driver.find_element_by_xpath('//*[@id="navbar-query"]')
    search_form.send_keys(title)
    search_form.send_keys(Keys.ENTER)
    sleep(2)

    movie = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]/a').get_attribute('href')
    driver.close()
    return movie[movie.find('/tt')+3:movie.find('/tt')+10]


def get_description_by_id(id):
    movie = imdb.get_movie(id)
    movie_description = movie.get('plot')
    movie_description = "".join(i for i in movie_description if i not in exclude)
    return movie_description.lower().replace('(', ' ').replace(')', ' ').replace('.', ' ')


def get_smart_word_vec(word):
    word_list = word.split(' ')
    for i in range(len(word_list)):
        word_list[i] = lemmatizer.lemmatize(word_list[i])
    new_str = ' '.join(word_list)
    return model.wv.word_vec(new_str)


def cosine_similarity(v1, v2):
    return (v1 @ v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def find_neighbours(id):
    neighbours = []
    vector = calculated_vectors[id_list.index(id)] if id in id_list else get_smart_word_vec(get_description_by_id(id))
    with Pool(2) as p:
        help_neighbours = p.map(partial(cosine_similarity, v2=vector), descr_vectors)
    for i in range(len(help_neighbours)):
        neighbours.append((i, help_neighbours[i]))
    neighbours.sort(key=itemgetter(1))
    neighbours.reverse()
    for i in range(20):
        neighbours[i] = neighbours[i][0]
    return neighbours[:20]


