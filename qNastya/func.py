from imdb import IMDb
import csv
import pandas as pd

N = 250
reader = pd.read_csv('~/PycharmProjects/movie_explorer/qNastya/qtop250_movie.csv')
loadedMovies = reader.values.tolist()

name_eng = [' '] * 250
movie_id = {}#[] * 250
cast = [0] * 100000
actorsBase = [0] * 100000
genresBase = [0] * 1000
genres = [0] * 1000

k = 0
z = 0

for i in range(N):
    selectedMovie = loadedMovies[i]
    name_eng[i] = selectedMovie[0]  # title
    cast[i] = selectedMovie[1].split(',')  # actors
    for j in range(len(cast[i])):
        cast[i][j] = cast[i][j].replace('[', '').replace(']', '')
    genres[i] = selectedMovie[2].split(',')  # genres
    for j in range(len(genres[i])):
        genres[i][j] = genres[i][j].replace('[', '').replace(']', '')

    #movie_id[i] = selectedMovie[3]  # url
    movie_id[name_eng[i]] = selectedMovie[3]  # url
    for j in range(len(cast[i])):
        actorsBase[k] = cast[i][j]  # записали всех подряд актеров
        k += 1

    for j in range(len(genres[i])):
        genresBase[z] = genres[i][j]
        z += 1

actorSet = set(actorsBase)
actorSet.remove(0)

genresSet = set(genresBase)
genresSet.remove(0)

def getIndexInSet(string, currentSet):
    resultIndex = 0
    for element in currentSet:
        if (string == element):
            return resultIndex
        resultIndex += 1

# фильм - вектор = берем фильм, смотрим его актерский состав:
# взяли одного актера нашли его индекс во множестве, поставили единичку на месте соответствующей координаты

filmVector = [[0] *( len(actorSet) + len(genresSet))for i in range(251)]
k = 0
filmRec = {}
namedFilms = {}

#build vectors
for i in range(0,N):
    movie = loadedMovies[i]
    currentCast = movie[1].split(',')
    for j in range(len(currentCast)):
        if (currentCast[j].replace('[', '').replace(']','') in actorSet):
            index = getIndexInSet(currentCast[j].replace('[', '').replace(']',''),actorSet)
            filmVector[i][index] = 1

    k = 0
    currentGenre = movie[2].split(',')
    for z in range(len(filmVector[i])-len(currentGenre)+1):
        if (k<len(currentGenre) and currentGenre[k].replace('[', '').replace(']','') in genresSet):
            index = getIndexInSet(currentGenre[k].replace('[', '').replace(']',''), genresSet)
            filmVector[i][z+index] = 1
        k += 1
    filmRec[movie[0]] = filmVector[i]

import math

def get_key(d, value):
    j = 0
    for k in d.keys():
        for v in d.values():
            if d[k] == value:
                return k

def get_norma(id):
    norma = {}
    index = id #getFilmIndex(film)
    currentFilm = filmVector[index]
    for i in range(1, N+1):
        if (i - 1 != index):
            sum = 0
            for j in range(1, len(actorSet)):
                sum += (filmVector[i - 1][j - 1] - currentFilm[j - 1]) * (filmVector[i - 1][j - 1] - currentFilm[j - 1])
            norma[get_key(filmRec, filmVector[i - 1])] = math.sqrt(sum)
        else:
            norma[get_key(filmRec, filmVector[i - 1])] = 800000
    return norma

def getFilmIndex(string):
    for i in range(len(loadedMovies)):
        if (string == loadedMovies[i][0]):
            return i

top20Recom = ['']*20
resultTitles = ['']*250

#find 20 films
def get_recommendation_list(string):
    currentIndex = getFilmIndex(string)
    from operator import itemgetter
    curList = []
    curList = get_norma(currentIndex)

    for j in range(0, len(curList) - 1):
        for i in range(0, len(curList) - j - 1):
            if curList[name_eng[i]] < curList[name_eng[i + 1]]:
                tmp = curList[name_eng[i+1]]
                curList[name_eng[i + 1]] = curList[name_eng[i]]
                curList[name_eng[i]] = tmp
    # вывод только 20 элементов
    endL = get_norma(currentIndex)

    tmpNorma = [0]*250
    for z in range(len(curList)):
        tmpNorma[z] = curList[name_eng[z]]

    for z in range(len(tmpNorma)):
        for g in range(len(endL)):
            if (tmpNorma[z] == endL[name_eng[g]]):
                resultTitles[z] = name_eng[g]

    k = len(curList) - 1
    j = 0
    for i in range(len(curList)):
        if (k >= len(curList) - 20 + 1):
            top20Recom[j] = resultTitles[k]
            k -= 1
            j += 1
    return top20Recom

result = ['']*20
def getUrlArr(arr):
    j = 0
    cur =['']*20
    for i in range(len(arr)):
        cur[j] = movie_id[arr[i]]
        j += 1
    tmp = set(cur)
    if ('' in tmp):
        tmp.remove('')
    result = list(tmp)
    return result

resultSet = set()
def get_recom_set(string):
    tmp = set(get_recommendation_list(string))
    if ('' in tmp):
        tmp.remove('')
    resultSet = list(tmp)
    return  resultSet

#print(get_recom_set("The Godfather: Part II"))
print(get_recommendation_list("The Godfather: Part II"))
#print('EEEEEEEE')
#print(getUrlArr(get_recom_set("The Godfather: Part II")))