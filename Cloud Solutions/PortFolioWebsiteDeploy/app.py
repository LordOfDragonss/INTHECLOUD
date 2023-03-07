import csv
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'
    
from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://miketool:r4FZbAmKDeHsOkPi@myowndatabase.31riann.mongodb.net/myFirstDatabase"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client["Test_dataBase"]



# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

   # Get the database
   dbname = get_database()

@app.route('/database.html', methods =('GET', 'POST'))
def databaseLoad():
    dbname = get_database()
    songs = dbname["Spotify_Songs"]
    songlist = songs.find()
    return render_template('database.html', songs = songlist)
