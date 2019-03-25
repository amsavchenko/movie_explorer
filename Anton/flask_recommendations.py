from project_movie_recommendations import find_neighbours, name_list, link_list, return_id_from_title

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def start():
    return render_template('start_page.html')


@app.route('/recommendation/', methods=['POST', 'GET'])
def help():
    if request.method == 'POST':
        title = request.form['Title']
        flash(title)
        return redirect(url_for('get_recommendation', id=return_id_from_title(title)))


@app.route('/get_recommendation/<id>', methods=['GET'])
def get_recommendation(id):
    title = get_flashed_messages()[0]
    neighbours = find_neighbours(id)
    return render_template('recommendation_page.html', title=title, id_list1=neighbours[:len(neighbours)//2],
                           id_list2=neighbours[len(neighbours)//2:], name_list=name_list, link_list=link_list)


if __name__ == "__main__":
    app.run(debug=True)