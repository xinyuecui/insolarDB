import os
import pandas as pd
import csv
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, current_app
)
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import logging
from werkzeug.exceptions import abort

from flaskr.auth import login_required


UPLOAD_FOLDER = 'flaskr/data'
ALLOWED_EXTENSIONS = {'xls','xlsx', 'csv'}

bp = Blueprint('contact', __name__)
current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(current_app)

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

@bp.route('/', methods=('GET', 'POST'))
def index():
    contacts = None
    numDocs = mongo.db.contact.count()
    startIdx, endIdx = 1,10
    if request.method == 'POST':
        startIdx = int(request.form['startidx'])
        endIdx = int(request.form['endidx'])

        error = None
    cursor = mongo.db.contact.find().limit(endIdx)
    # logger.info(contacts)
    if cursor:
        # extract the list of documents from cursor obj
        mongo_docs = list(cursor)[startIdx:endIdx]


        # create an empty DataFrame for storing documents
        docs = pd.DataFrame(columns=[])

        # iterate over the list of MongoDB dict documents
        for num, doc in enumerate(mongo_docs):
            doc["_id"] = str(doc["_id"]) # convert ObjectId() to str
            doc_id = doc["_id"]

            # create a Series obj from the MongoDB dict
            series_obj = pd.Series(doc, name=doc_id)

            docs = docs.append(series_obj)

        # export the MongoDB documents as a JSON file
        contacts = docs.to_html()

    return render_template('contact/index.html', contacts=contacts, numDocs=numDocs,startIdx=startIdx, endIdx=endIdx)

@bp.route('/search', methods=('GET', 'POST'))
def search():
    search_result = None
    if request.method == 'POST':
        name = request.form['person']
        phone = request.form['phone']
        email = request.form['email']
        error = None

        if not name and not phone and not email:
            error = 'Keyword is required.'

        if error is not None:
            flash(error)
        else:
            if name:
                search_result = mongo.db.contact.find_one({"Name": name})
            elif phone:
                search_result = mongo.db.contact.find_one({"Phone": phone})
            elif email:
                search_result = mongo.db.contact.find_one({"Email": email})
            return render_template('contact/search.html', search_result=search_result)

    return render_template('contact/search.html', search_result=search_result)


def file_type(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and \
           file_type(filename) in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=('GET', 'POST'))
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected!')
            return redirect(request.url)


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('Successfully uploaded ' + filename + '!')
            return redirect(url_for('contact.uploaded_file',
                                    filename=filename))
    return render_template('contact/upload.html')


@bp.route('/upload/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    f = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    with open(f) as file:
        if file_type(filename) == 'csv':
            data = pd.read_csv(file, header=0, engine='python')
        else:
            data = pd.read_excel(file, header=0)

    return render_template('contact/display.html', filename=filename, data=data.to_html(index=False))