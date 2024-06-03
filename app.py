from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_pymongo import PyMongo
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

@app.route('/')
def home():
    files = mongo.db.uploads.find()
    return render_template('home.html', files=files)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/other_option1')
def other_option1():
    return render_template('other_option1.html')

@app.route('/other_option2')
def other_option2():
    return render_template('other_option2.html')

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            mongo.db.uploads.insert_one({'filename': filename, 'upload_time': datetime.now()})
            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads')
def uploaded_files():
    files = mongo.db.uploads.find()
    return render_template('uploaded_files.html', files=files)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0", post=80)
