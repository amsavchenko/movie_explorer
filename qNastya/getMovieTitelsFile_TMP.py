from imdb import IMDb
import csv
import pandas as pd
reader = pd.read_csv('~/PycharmProjects/movie_explorer/qNastya/qtop250_movie.csv')

# берем все значениея, вызываем tolist() - получаем фактически то, что возвращает метод get_movies()
loadedMovies = reader.values.tolist()

allTitles = [' ']*250

for i in range(250):
    selectedMovie = loadedMovies[i]
    allTitles[i] = selectedMovie[0]  # title
for i in range(250):
    print(allTitles[i])