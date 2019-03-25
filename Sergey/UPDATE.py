import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.stem import WordNetLemmatizer
import string
from imdb import IMDb

imdb = IMDb()

flag = [False]


def ID_parser():
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short',
              'Sport', 'Superhero', 'Thriller', 'War', 'Western']
    IDs = []
    for i in genres:
        start = 51

        url = 'https://www.imdb.com/search/title?genres='
        url += i.lower()
        url += '&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=17d3863a-3e07-4c9b-a09a-f643edc8e914&pf_rd_r=76J9GQPSD6DDJM018W0X&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_1'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for j in range(len(soup.find_all('h3', {'class': 'lister-item-header'}))):
            a = soup.find_all('h3', {'class': 'lister-item-header'})[j].find('a').get('href')
            IDs.append(a[a.find('tt') + 2:a.find('tt') + 9])

        while start < 560:
            url = 'https://www.imdb.com/search/title?genres='
            url += i.lower()
            url += '&start='
            url += str(start)
            url += '&explore=title_type,genres&ref_=adv_nxt'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for k in range(len(soup.find_all('h3', {'class': 'lister-item-header'}))):
                a = soup.find_all('h3', {'class': 'lister-item-header'})[k].find('a').get('href')
                IDs.append(a[a.find('tt') + 2:a.find('tt') + 9])

            start += 50
    return IDs


def get_description_and_genres_by_ID(id):
    movie = imdb.get_movie(id)
    imdb.update(movie, info=['main'])
    movie_description = str(movie.get('plot'))
    movie_description += str(movie.get('plot outline'))
    movie_genres = movie.get('genres')
    return [movie_description.lower(), movie_genres]


def make_dataset(ids):
    ids = set(ids)
    df = pd.DataFrame(list(ids), columns=['ID'])

    df['Description'] = 0

    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short',
              'Sport', 'Superhero', 'Thriller', 'War', 'Western']
    for i in genres:
        df[i] = 0

    for i in range(len(df['ID'])):
        descr_genre = get_description_and_genres_by_ID(df['ID'].loc[i])
        df['Description'].loc[i] = descr_genre[0]
        if descr_genre[1] is not None:
            for genre in descr_genre[1]:
                if genre in genres:
                    df[genre].loc[i] = 1
        print(i)

    #df.to_csv('Description.csv', sep=',')
    df.to_csv('~/PycharmProjects/movie_explorer/Sergey/Description.csv', sep=',')


def UPDATE():
    global flag
    flag[0] = True

    ID = ID_parser()
    make_dataset(ID)

    #data = pd.read_csv('Description.csv', sep=',',
                   # dtype={'ID': str, 'Description': str, 'Action': int, 'Adventure': int, 'Animation': int,
                #            'Biography': int, 'Comedy': int, 'Crime': int, 'Documentary': int, 'Drama': int,
                 #           'Family': int, 'Fantasy': int, 'Film Noir': int, 'History': int, 'Horror': int,
                  #          'Music': int, 'Musical': int, 'Mystery': int, 'Romance': int, 'Sci-Fi': int,
                   #         'Short': int, 'Sport': int, 'Superhero': int, 'Thriller': int, 'War': int,
                    #        'Western': int}, index_col=0)

    data = pd.read_csv('~/PycharmProjects/movie_explorer/Sergey/Description.csv', sep=',',
                    dtype={'ID': str, 'Description': str, 'Action': int, 'Adventure': int, 'Animation': int,
                            'Biography': int, 'Comedy': int, 'Crime': int, 'Documentary': int, 'Drama': int,
                            'Family': int, 'Fantasy': int, 'Film Noir': int, 'History': int, 'Horror': int,
                            'Music': int, 'Musical': int, 'Mystery': int, 'Romance': int, 'Sci-Fi': int,
                            'Short': int, 'Sport': int, 'Superhero': int, 'Thriller': int, 'War': int,
                            'Western': int}, index_col=0)
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
            'Fantasy', 'Film Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
            'Short', 'Sport', 'Superhero', 'Thriller', 'War', 'Western']

    for i in range(len(data['ID'])):
        if data['Description'].loc[i] == 'none':
            desc_genre = get_description_and_genres_by_ID(data['ID'].loc[i])
            data['Description'].loc[i] = desc_genre[0]
            if desc_genre[1] is not None:
                for genre in desc_genre[1]:
                    if genre in genres:
                        data[genre].loc[i] = 1

    lemmatizer = WordNetLemmatizer()
    exclude = set(string.punctuation)

    data['Description'] = data['Description'].apply(lambda x: "".join(i for i in x if i not in exclude))
    data['Description'] = data['Description'].apply(lambda x: " ".join(lemmatizer.lemmatize(i) for i in x.split()))

    data.to_csv('~/PycharmProjects/movie_explorer/Sergey/DESCRIPTIONS and GENRES.csv', sep=',')

    flag[0] = False
