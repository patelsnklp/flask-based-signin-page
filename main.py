from flask import Flask, request, render_template
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB connection setup
uri = "mongodb+srv://my_username:my_passowrd@cluster0.6ltcang.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("MongoDB connection error:", e)

# Use this working client
db = client["test"]
collection = db["flask-tutorial"]

@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.today().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/submit', methods=["POST"])
def submit():
    form_data = dict(request.form)
    collection.insert_one(form_data)
    return {"message": "Data submitted successfully"}


if __name__ == '__main__':
    app.run(debug=True)
