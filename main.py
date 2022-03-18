import requests
from random import randrange
from PIL import Image
from PIL import ImageFilter
import os
import datetime
import csv



def app():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    today = str(datetime.date.today() + datetime.timedelta(days=1))
    cwd = os.getcwd()
    folder = os.path.join(THIS_FOLDER, 'static/' + today)
    try:
        os.mkdir(folder)
    except:
        print('folder already exists')

    url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=7259b8c0cf2f62da6123fb0ea2dcc35e&format=json"


    response = requests.request("GET", url)

    data = response.json()

    artist = data['artists']['artist'][int(randrange(49))]['name']

    url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=" + artist +"&api_key=7259b8c0cf2f62da6123fb0ea2dcc35e&format=json"

    response = requests.request("GET", url)

    data = response.json()


    albumname = data['topalbums']['album'][0]['name']
    albumart = data['topalbums']['album'][0]['image'][3]['#text']
    artistname = data['topalbums']['album'][0]['artist']['name']


    answer = albumname + ', ' + artistname
    albumlist = []
    with open(os.path.join(THIS_FOLDER, 'albums.csv'), 'r') as file:
        reader = csv.reader(file)
        for i in reader:
            albumlist.append(i[0])

    if answer in albumlist:
        print('already in there, trying again')
        app()

    else:
        print('adding to csv', answer)
        with open(os.path.join(THIS_FOLDER, 'albums.csv'), 'a') as file:
            writer = csv.writer(file)
            writer.writerow([answer])


        f = open(os.path.join(THIS_FOLDER, 'static/' + today + '/data.csv'), 'w+')

        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow([albumname, artistname])

        # close the file
        f.close()


        tempname = "temp.jpeg"

        img_data = requests.get(albumart).content
        with open(os.path.join(THIS_FOLDER, tempname), 'wb') as handler:
            handler.write(img_data)


        # Open existing image
        OriImage = Image.open(os.path.join(THIS_FOLDER, tempname))
        blurriness = [0, 5, 10, 20, 30, 40, 50]
        for i in blurriness:
            boxImage = OriImage.filter(ImageFilter.BoxBlur(i))
            rgb_im = boxImage.convert('RGB')
            rgb_im.save(os.path.join(THIS_FOLDER, 'static/' + today + '/image' + str(i) + '.jpg'))
        os.remove(os.path.join(THIS_FOLDER, 'temp.jpeg'))

app()