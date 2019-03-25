
from Sasha import create_assessment
from Anton import project_movie_recommendations
from Sergey import UPDATE as upd
from Sergey import Classifier as CLS

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask import Flask, request, jsonify,json, Response, render_template
from qNastya import func
from flask import redirect, url_for, flash, get_flashed_messages


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/input-film-assessment')
def res():
        return render_template('input-film-assessment.html')


@app.route('/recommendation-for-film', methods=['POST', 'GET'])
def help_1():
        return render_template('start_page.html')


@app.route('/film-assessment', methods = ['POST', 'GET'])
def result_1():
    if request.method == 'POST':
        my_result = request.form
        title = my_result['Name']
        res = {}
        assesment = create_assessment.assessment(title)
        print(assesment)
        if int(assesment) == 1:
                res['Name'] = 'Our system says the movie "'+ title +'" will be interesting'
        elif int(assesment) == 0:
                res['Name'] = 'Our system has determined that the movie "'+ title +'" will not be so exciting'  
        else:
                res['Name'] = 'Sorry, no movie details were found'

        return render_template('film-assessment.html', result = res)


@app.route('/recommendation', methods=['POST', 'GET'])
def help():
        title = request.form['Title']
        flash(title)
        id=project_movie_recommendations.return_id_from_title(title)
        title = get_flashed_messages()[0]
        neighbours = project_movie_recommendations.find_neighbours(id)
        count = ''
        return render_template('recommendation_page.html', count = count, title=title,
                               id_list1=neighbours[:len(neighbours)//2], id_list2=neighbours[len(neighbours)//2:],
                               name_list=project_movie_recommendations.name_list,
                               link_list=project_movie_recommendations.link_list)


@app.route('/genre-predict', methods=['POST', 'GET'])
def start_1():
    return render_template('start_page_Sergey.html')


@app.route('/genre-predict-res', methods=['POST', 'GET'])
def help_id():
    if request.method == 'POST':
        title = request.form['Title']
        flash(title)
        id=CLS.return_id_from_title(title)
        title = get_flashed_messages()[0]
        genres = CLS.Genres_Prediction_by_ID(id)
        return render_template('genres_page.html', title=title, genres=genres)


@app.route('/genres-description', methods=['POST', 'GET'])
def help_descr():
    if request.method == 'POST':
        descr = request.form['Description']
        flash(descr)
        description=descr
        genres = CLS.Genres_Prediction_by_Description(description)
        return render_template('genres_page_descr.html', title=description, genres=genres)


@app.route('/process_data/' , methods=['POST', 'GET'])
def update():
    upd.UPDATE()


@app.route('/rec-actors')
def hello():
    return render_template('start-rec-actors.html')


@app.route('/rec-actors-res', methods=['POST', 'GET'])
def help_2():
    if request.method == 'POST':
        title = request.form['Title']
        print(title)
        flash(title)
        title=title
        title = get_flashed_messages()[-1]
        neighbours = func.get_recom_set(title)[:20]#get_recommendation_list(title)
        current_links = func.getUrlArr(neighbours)
        return render_template('recommendations.html', title=title, id_list1=neighbours[:len(neighbours)//2],
                           id_list2=neighbours[len(neighbours)//2:], top20Recom=func.top20Recom, result=func.result)


if __name__=="__main__":
    app.run(debug = True)
