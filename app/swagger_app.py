import fire
import spacy
from modules.spellchecker import SpellChecker
from modules.parser.pdf_parser import PDFParser

import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import connexion


def main(resume_file):
    parser = PDFParser(resume_file)
    spell_checker = SpellChecker()
    possible_spelling_errors = list(spell_checker.check_misspelled(parser.text))
    parsed_dict = {"email": parser.email,
                   "name": parser.name,
                   "phone_no": parser.phone,
                   "sections": parser.sections,
                   "possible_spelling_errors":possible_spelling_errors}
    return parsed_dict


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
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if ! os.path.exist(config['UPLOAD_FOLDER']):
                os.makedirs(config['UPLOAD_FOLDER'])
            out_filename = os.path.join(config['UPLOAD_FOLDER'], filename)
            file.save(out_filename)
            import json
            return jsonify(main(out_filename))
            # return '''
            # <!doctype html>
            # <title>Done</title>
            # '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

UPLOAD_FOLDER = 'test/upload'
ALLOWED_EXTENSIONS = set([ 'pdf'])

# app = Flask(__name__)
config = {}
config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             out_filename = os.path.join(config['UPLOAD_FOLDER'], filename)
#             file.save(out_filename)
#             import json
#             return jsonify(main(out_filename))
#             # return '''
#             # <!doctype html>
#             # <title>Done</title>
#             # '''
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#

if __name__ == "__main__":
    app.run(debug=True)
