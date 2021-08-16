import warnings
import json
from flask import Flask, render_template,request,jsonify,Response, redirect, url_for
warnings.filterwarnings("ignore")
from text_generator import get_output_sequence
from data_extractor import viewData,get_data
from news_filter import load_json,load_table
import os
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search/', methods = ['POST'])
def search():
	data =  request.form.get('search_param')
	# return render_template('result.html',result=result)
	return redirect(url_for("result", data=data))

@app.route('/search/<data>')
def result(data):
	result=get_output_sequence(data)
	# return render_template('result.html',result=result,mimetype='application/json')
	return Response(result,mimetype='application/json')

@app.route('/explore_extracted/')
def explore():
    result=viewData()
    return Response(result,mimetype='application/json')

@app.route('/extract')
def extract():
    get_data()
    result=viewData()
    return result.to_html()

@app.route('/classifier_json')
def classifier_json():
    result=load_json()
    return Response(result,mimetype='application/json')

@app.route('/classifier_table')
def classifier_table():
    result=load_table()
    return result.to_html()

if __name__ == '__main__':
	app.run()

