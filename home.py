from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/aboutMe")
def aboutMe():
    return render_template('aboutme.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/register")
def registerInterest():
    return render_template('register.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/fileUpload", methods=['GET', 'POST'])
def fileUpload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('success'))
        else:
            # Redirect to the error page for incorrect file format
            return redirect(url_for('error'))

    return render_template('fileUpload.html')
    
@app.route('/list_files')
def list_files():
    # Get the list of uploaded files
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('list_files.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)