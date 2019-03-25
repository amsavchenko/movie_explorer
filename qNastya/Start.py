from flask import Flask, request, jsonify,json, Response, render_template
from func import getFilmIndex, name_eng, movie_id, get_recom_set, get_recommendation_list, top20Recom, getUrlArr, result
from flask import redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello():
    return render_template('start.html')


@app.route('/recommendations/', methods=['POST', 'GET'])
def help():
    if request.method == 'POST':
        title = request.form['Title']
        print(title)
        flash(title)
        return redirect(url_for('get_recommendation', title=title))

@app.route('/get_recommendation/<title>', methods=['GET'])
def get_recommendation(title):
    title = get_flashed_messages()[0]
    print(title)
    neighbours = get_recom_set(title)[:20]#get_recommendation_list(title)
    print(neighbours)
    #print('fefefefe')
    #print(get_recommendation_list(title))
    current_links = getUrlArr(neighbours)
    print(current_links)
    # urlArr = ['']*len(neighbours)
    # for i in range(len(urlArr)):
    #     urlArr[i] = movie_id[neighbours[i]]
    #     print(neighbours[i], ' ', urlArr[i])
    return render_template('recommendations.html', title=title, id_list1=neighbours[:len(neighbours)//2],
                           id_list2=neighbours[len(neighbours)//2:], top20Recom=top20Recom, result=result)


if __name__=="__main__":
    app.run(debug = True, port = 5002)