import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from imdb import IMDb
imdb = IMDb()
import string


from selenium.webdriver import Chrome 
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def return_id_from_title(title):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    chrome_driver_binary = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

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


def Genres_Prediction_by_ID(ID):
    stopWords = set(stopwords.words('english'))
    data = pd.read_csv('~/PycharmProjects/movie_explorer/Sergey/DESCRIPTIONS and GENRES.csv', sep=',',
                       dtype={'ID': str, 'Description': str, 'Action': int, 'Adventure': int, 'Animation': int,
                              'Biography': int, 'Comedy': int, 'Crime': int, 'Documentary': int, 'Drama': int,
                              'Family': int, 'Fantasy': int, 'Film Noir': int, 'History': int, 'Horror': int,
                              'Music': int, 'Musical': int, 'Mystery': int, 'Romance': int, 'Sci-Fi': int, 'Short': int,
                              'Sport': int, 'Superhero': int, 'Thriller': int, 'War': int, 'Western': int}, index_col=0)
    flag = -1
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport',
              'Thriller', 'War', 'Western']

    for i in range(len(data['ID'])):
        if data['ID'].loc[i] == ID:
            flag = i

    if flag == -1:
        df = pd.DataFrame([ID], columns=['ID'], index={len(data['ID'])})

        movie = imdb.get_movie(ID)
        imdb.update(movie, info=['main'])
        movie_description = str(movie.get('plot'))
        movie_description += str(movie.get('synopsis'))
        movie_description += str(movie.get('plot outline'))
        movie_genres = movie.get('genres')

        df['Description'] = movie_description.lower()

        lemmatizer = WordNetLemmatizer()
        exclude = set(string.punctuation)

        df['Description'] = df['Description'].apply(lambda x: "".join(i for i in x if i not in exclude))
        df['Description'] = df['Description'].apply(lambda x: " ".join(lemmatizer.lemmatize(i) for i in x.split()))

        for genre in genres:
            df[genre] = 0

        for genre in movie_genres:
            if genre in genres:
                df[genre] = 1

        flag = len(data['ID'])
        data = data.append(df, sort=True)

    description = data.loc[0:, 'Description']
    tfidf_transformer = TfidfTransformer()
    vectorizer = CountVectorizer(stop_words=stopWords).fit(description)
    features = tfidf_transformer.fit_transform(vectorizer.transform(description))
    clf = LogisticRegression(C=0.8, solver='liblinear', penalty='l1', intercept_scaling=10,
                             class_weight={1: 10, 0: 1})

    GENRES = []

    for genre in genres:
        target = data.loc[0:, genre]
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.75, random_state=42)

        clf.fit(X_train, y_train)

        FEATURES = features[flag]

        prediction = clf.predict(FEATURES)

        if prediction[0] == 1:
            GENRES.append(genre)
    return GENRES


def Genres_Prediction_by_Description(descr):
    stopWords = set(stopwords.words('english'))
    #data = pd.read_csv('DESCRIPTIONS and GENRES.csv', sep=',',
     #                  dtype={'ID': str, 'Description': str, 'Action': int, 'Adventure': int, 'Animation': int,
      #                        'Biography': int, 'Comedy': int, 'Crime': int, 'Documentary': int, 'Drama': int,
       #                       'Family': int, 'Fantasy': int, 'Film Noir': int, 'History': int, 'Horror': int,
        #                      'Music': int, 'Musical': int, 'Mystery': int, 'Romance': int, 'Sci-Fi': int, 'Short': int,
         #                     'Sport': int, 'Superhero': int, 'Thriller': int, 'War': int, 'Western': int}, index_col=0)
    data = pd.read_csv('~/PycharmProjects/movie_explorer/Sergey/DESCRIPTIONS and GENRES.csv', sep=',',
                       dtype={'ID': str, 'Description': str, 'Action': int, 'Adventure': int, 'Animation': int,
                              'Biography': int, 'Comedy': int, 'Crime': int, 'Documentary': int, 'Drama': int,
                              'Family': int, 'Fantasy': int, 'Film Noir': int, 'History': int, 'Horror': int,
                              'Music': int, 'Musical': int, 'Mystery': int, 'Romance': int, 'Sci-Fi': int, 'Short': int,
                              'Sport': int, 'Superhero': int, 'Thriller': int, 'War': int, 'Western': int}, index_col=0)
    
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport',
              'Thriller', 'War', 'Western']

    df = pd.DataFrame(['none'], columns=['ID'], index={len(data['ID'])})

    df['Description'] = descr.lower()

    lemmatizer = WordNetLemmatizer()
    exclude = set(string.punctuation)

    df['Description'] = df['Description'].apply(lambda x: "".join(i for i in x if i not in exclude))
    df['Description'] = df['Description'].apply(lambda x: " ".join(lemmatizer.lemmatize(i) for i in x.split()))

    for genre in genres:
        df[genre] = 0

    data = data.append(df, sort=True)

    description = data.loc[0:, 'Description']
    tfidf_transformer = TfidfTransformer()
    vectorizer = CountVectorizer(stop_words=stopWords).fit(description)
    features = tfidf_transformer.fit_transform(vectorizer.transform(description))
    clf = LogisticRegression(C=0.8, solver='liblinear', penalty='l1', intercept_scaling=10,
                             class_weight={1: 10, 0: 1})

    GENRES = []

    for genre in genres:
        target = data.loc[0:, genre]
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.75, random_state=42)

        clf.fit(X_train, y_train)

        FEATURES = features[len(data['ID']) - 1]

        prediction = clf.predict(FEATURES)

        if prediction[0] == 1:
            GENRES.append(genre)
    return GENRES