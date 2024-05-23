import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing  import image
import tensorflow as tf
from flask import Flask , request, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])		
def predict():
    model_name=""
    excel_name=""
    plant=request.form['plant']
    if(plant=="vegetable"):
        model_name=r"ensemble_model.h5"
        excel_name='precautions - vegetables.xlsx'
    elif(plant=="fruit"):
        model_name=r"best_xception.h5"
        excel_name='precautions - fruits.xlsx'
    a = request.files['image']
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath,'uploads',a.filename)
    a.save(filepath)
    img = image.load_img(filepath,target_size = (64,64))
    model = load_model (model_name)
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis = 0)
    p=model.predict(x)
    pred = np.argmax(model.predict(x))
    df=pd.read_excel(excel_name)
    return render_template("index.html", result=df.iloc[pred.item(),0])
        
if __name__ == '__main__':
    app.run(debug = True, threaded = False)