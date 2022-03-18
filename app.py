from flask import Flask, render_template, request, url_for
from datetime import date
import csv
import os
app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def game():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    today = date.today()
    startdate = date(2022, 3, 13)
    delta = today - startdate
    albumlist = []

    with open(os.path.join(THIS_FOLDER, 'albums.csv'), 'r') as file:
        reader = csv.reader(file)
        for i in reader:
            albumlist.append(i[0])

    with open(os.path.join(THIS_FOLDER, 'static/' + str(today) + '/data.csv'), 'r') as file:
        reader = csv.reader(file)
        answerls = []
        for i in reader:
            answerls.append(i)

    answer = answerls[0][0] + ', ' + answerls[0][1]

    if answer not in albumlist:
        albumlist.append(answer)
        albumlist.sort()


    if request.method == 'GET':
        image = url_for('static', filename=str(today) + '/image50.jpg')
        return render_template('game.html', guess=0, image=image, answer=answer, albumlist=albumlist, daynr=delta.days)

    if request.method == 'POST':
        guess = request.form['guess']
        input = request.form['input']

        if input == answer:
            return render_template('done.html', guess=int(guess) + 1, image=url_for('static', filename=str(today) + '/image0.jpg'), answer=answer, daynr=delta.days)
        else:
            nextguess = int(guess) + 1

            if nextguess == 1:
                newimage = url_for('static', filename=str(today) + '/image40.jpg')
            if nextguess == 2:
                newimage = url_for('static', filename=str(today) + '/image30.jpg')
            if nextguess == 3:
                newimage = url_for('static', filename=str(today) + '/image20.jpg')
            if nextguess == 4:
                newimage = url_for('static', filename=str(today) + '/image10.jpg')
            if nextguess == 5:
                newimage = url_for('static', filename=str(today) + '/image5.jpg')

            if nextguess == 6:
                #FAILED
                return render_template('failed.html', guess=guess, image=url_for('static', filename=str(today) + '/image0.jpg'), answer=answer, daynr=delta.days)

            return render_template('game.html', guess=nextguess, image=newimage, answer=answer, albumlist=albumlist, daynr=delta.days)