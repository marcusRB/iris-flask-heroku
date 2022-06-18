'''
DOC STRING
author
date
description

'''
from flask import Flask, session, url_for, render_template, redirect
import joblib

from flower_form import FlowerForm

# Cargamos los modelos guardados en saved_models
knn_loaded = joblib.load("saved_models/knn_iris_dataset.pkl")
encoder_loaded = joblib.load("saved_models/iris_label_encoder.pkl")

# Creamos la función de predicción
def make_prediction(model, encoder, sample_json):
    '''
    Doc string
    '''
    SepalLengthCm = sample_json['SepalLengthCm']
    SepalWidthCm = sample_json['SepalWidthCm']
    PetalLengthCm = sample_json['PetalLengthCm']
    PetalWidthCm = sample_json['PetalWidthCm']

    # Creamos un vector de input
    flower = [[SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm]]

    # Predicción
    prediction_raw = model.predict(flower)

    # Convertimos los índices en labels de las clases
    prediction_real = encoder.inverse_transform(prediction_raw)

    return prediction_real[0]

# creamos la app de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET','POST'])
def index():
    '''
    Doc string
    '''
    form = FlowerForm()

    if form.validate_on_submit():
        session['SepalLengthCm'] = form.SepalLengthCm.data
        session['SepalWidthCm'] = form.SepalWidthCm.data
        session['PetalLengthCm'] = form.PetalLengthCm.data
        session['PetalWidthCm'] = form.PetalWidthCm.data

        return redirect(url_for('prediction'))
    return render_template("home.html", form=form)

@app.route('/prediction', methods=['POST','GET'])
def prediction():
    '''
    Doc string
    '''
    content = {'SepalLengthCm': float(session['SepalLengthCm']),
    'SepalWidthCm': float(session['SepalWidthCm']),
               'PetalLengthCm': float(session['PetalLengthCm']),
               'PetalWidthCm': float(session['PetalWidthCm'])}

    results = make_prediction(knn_loaded, encoder_loaded, content)

    return render_template('prediction.html', results=results)

# Ejecutamos la aplicación app.run()
if __name__ == '__main__':
    # LOCAL
    # app.run(host='0.0.0.0', port=8080)

    # REMOTO
    app.run()
