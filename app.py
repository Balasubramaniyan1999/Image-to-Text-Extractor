import cv2
import os,pytesseract
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template
from os.path import join, dirname, realpath



UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/..')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



#app configuration
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"


#OCR Engine path
engine_path =  r'D:\GECS_Final\Tesseract-OCR\tesseract.exe'



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/extract',methods=['GET','POST'])
def extract():
    file = request.files['file']
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
            pytesseract.pytesseract.tesseract_cmd = engine_path
            custom_config = r'--oem 3 --psm 6'
            msg = pytesseract.image_to_string(img, config=custom_config, lang="eng")
        except Exception as e:
            msg = e
    return render_template('home.html',output = msg)


if __name__ == '__main__':
    app.run(debug=True)