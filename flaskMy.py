from flask import Flask
from flask import send_from_directory
from main import main
import os,time
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import IDReader


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_information(directory):
    file_list = []
    for i in os.listdir(directory):
        a = os.stat(os.path.join(directory,i))
        file_list.append([i,time.ctime(a.st_ctime)]) #[file,created]
    return file_list

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory("./files", "template_final.xls")
    
@app.route('/uploadsIdPass/<name>')
def download_file_IdPass(name):
    return send_from_directory("./pdf_files", "template_IdPassFinal.xls")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                main(filename)
                return redirect(url_for('download_file', name=filename))
        elif 'IdPass' in request.files:
            file = request.files['IdPass']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                IDReader.main(filename)
                return send_from_directory("./files", "template_IdPassFinal.xls")

        else: 
            flash('No file part')
            return redirect(request.url)
        

    return  render_template('upload.html')

@app.route("/")
def hello_world():
    return render_template('index.html')
     
@app.route('/logs/')
def logs():
    #filenames = os.listdir('uploads')
    filenames = get_information("uploads")
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