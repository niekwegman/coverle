import requests
from random import randrange
from PIL import Image
from PIL import ImageFilter
import os
import datetime
import csv



def app():
    today = str(datetime.date.today() + datetime.timedelta(days=1))
    cwd = os.getcwd()
    folder = os.path.join(cwd, 'static/' + today)
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
    with open('albums.csv', 'r') as file:
        reader = csv.reader(file)
        for i in reader:
            albumlist.append(i[0])
    print(albumlist)

    if answer in albumlist:
        print('already in there, trying again')
        app()

    else:
        print('adding to csv', answer)
        with open('albums.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([answer])


        f = open('static/' + today + '/data.csv', 'w+')

        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow([albumname, artistname])

        # close the file
        f.close()


        tempname = "temp.jpeg"

        img_data = requests.get(albumart).content
        with open(tempname, 'wb') as handler:
            handler.write(img_data)


        # Open existing image
        OriImage = Image.open(tempname)
        blurriness = [0, 5, 10, 20, 30, 40, 50]
        for i in blurriness:
            boxImage = OriImage.filter(ImageFilter.BoxBlur(i))
            rgb_im = boxImage.convert('RGB')
            rgb_im.save('static/' + today + '/image' + str(i) + '.jpg')
        os.remove('temp.jpeg')

app()