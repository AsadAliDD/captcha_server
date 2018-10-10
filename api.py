import flask
from flask import request, jsonify
import base64
import captcha 
import base64
from PIL import Image
import cv2
from StringIO import StringIO
import numpy as np
import uuid


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Captcha API</h1><p>This site is a prototype API for Captcha solver.</p>"



@app.route('/upload', methods=['POST']) 
def upload_base64_file(): 
    """ 
        Upload image with base64 format and get car make model and year 
        response 
    """

    data = request.form.get('img')

    if data is None:
        print("No valid request body, json missing!")
        return jsonify({'error': 'No valid request body, json missing!'})
    else:
        
        path=convert(data)
        cords=captcha.main('temp_bin.jpg',path)
        if(cords==0):
            output=str(0)+","+str(0)
            record(path,output)
            return jsonify({'Failure': output}) 
        
        x=(cords[0]+cords[1])/2.0
        y=(cords[2]+cords[3])/2.0
        output=str(x)+","+str(y)
        record(path,output)
        return jsonify({'Success': output})
        



def readb64(base64_string,ext):
    sbuf = StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    filename=str(uuid.uuid4().hex)[:10]+'.'+ext
    path='./images/'+filename
    print filename
    pimg.save(path)
    return path
    

def convert(b64):
    extension=b64[b64.find('/')+1:b64.find(';')]
    img=b64[b64.find(',')+1:]
    path=readb64(img,extension)
    return path

    
def record(path,status):
    ofile=open('record.csv','a')
    ofile.write(path)
    ofile.write(',')
    ofile.write(status)
    ofile.write('\n')
    ofile.close()
    




app.run()