from flask import Flask
from flask import send_from_directory
from main import main
import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<name>')
def download_file(name):
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    return send_from_directory("./pdf_files", "template.xls_final.xls")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main(filename)
            return redirect(url_for('download_file', name=filename))
    return  render_template('upload.html')

@app.route("/")
def hello_world():
    return "<p style='white-space: pre-line'>Veuillez aller sur /upload pour télécharger un nouveau fichier. \n Please go to /upload for uploading a new file</p>"

@app.route('/logs/')
def logs():
    filenames = os.listdir('uploads')
    return render_template('logs.html', files=filenames)

@app.route('/logs/<path:filename>')
def log(filename):
    return send_from_directory(
        os.path.abspath('uploads'),
        filename,
        as_attachment=True
    )
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__ == '__main__':
    app.run(debug=True)