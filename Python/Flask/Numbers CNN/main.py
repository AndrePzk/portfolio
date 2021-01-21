from flask import Flask, request, render_template, redirect, url_for
from keras.models import load_model
import numpy as np


app = Flask(__name__)

m0 = []
for i in range(28) :
    m0.append(list(np.zeros([28])))

pred = ""
pred_do = False
first_rnd = True
res = ""
conf = ""




model = load_model('static/number_model.h5py')

@app.route('/', methods=['GET', 'POST'])

def home():

    global pred, m0, pred_do, first_rnd, res, conf

    

    if pred_do :
        data = np.array(m0).reshape(-1, 28, 28, 1)
        pred = model.predict(data)
        pred = np.round_(pred, 3) * 100
        if np.amax(pred) > 50 :
            res = int(np.where(pred == np.amax(pred))[1])
            conf = str(np.trunc(np.amax(pred)*10)/10) + "%"
        else :
            res = ":("
            conf = "je ne sais pas"
    else :
        pred = [[0,0,0,0,0,0,0,0,0,0]]

    if first_rnd and pred_do :
        first_rnd = False
        return redirect(url_for('home'))

    return render_template('index.html', matrix=m0, prediction=pred, result=res, confidence=conf, h0=pred[0][0], h1=pred[0][1], h2=pred[0][2], h3=pred[0][3], h4=pred[0][4], h5=pred[0][5], h6=pred[0][6], h7=pred[0][7], h8=pred[0][8], h9=pred[0][9])

@app.route('/predict', methods=['GET', 'POST'])

def predict():

    global pred, m0, pred_do

    m0 = request.get_json()
    m0 = m0['matrix']

    pred_do = True

    return "True"

if __name__ == "__main__":
    app.run()