import pickle
from keras.models import load_model
import pandas as pd
import sqlalchemy
import re
import tensorflow as tf 
from sqlalchemy import create_engine



def initialize_values():
	tokenizer = pickle.load(open("tokenizer.pickle", "rb"))
	model = load_model('model.h5')
	db_name = "news_data.db"
	table_name = "News"
	engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
	df = pd.read_sql_table(table_name, engine)
	return tokenizer, model, df

def normalize(data):
	normalized = []
	for i in data:
	    i = i.lower()
	    # get rid of urls
	    i = re.sub('https?://\S+|www\.\S+', '', i)
	    # get rid of non words and extra spaces
	    i = re.sub('\\W', ' ', i)
	    i = re.sub('\n', '', i)
	    i = re.sub(' +', ' ', i)
	    i = re.sub('^ ', '', i)
	    i = re.sub(' $', '', i)
	    normalized.append(i)
	return normalized

def process_and_predict():
	tokenizer,model,df=initialize_values()
	X_test = df['Description']
	X_test=normalize(X_test)
	X_test = tokenizer.texts_to_sequences(X_test)
	X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, padding='post', maxlen=256)
	df['label']='False'
	binary_predictions=[]
	predictions = model.predict(X_test)
	for i in predictions:
	    if(i<0.5):
	    	binary_predictions.append('False')
	    else:
	    	binary_predictions.append('True')
	df['label']=binary_predictions
	news=df.loc[df['label']=='True']
	del news['label']
	del news['index']
	print(news.shape)
	save_database(news)
	

def save_database(df):
	sqlite_connection,sqlite_table,engine=sqlengine()
	df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')

def sqlengine():
	engine = create_engine('sqlite:///actual_news_data.db', echo=True)
	sqlite_connection = engine.connect()
	sqlite_table = "News"
	return sqlite_connection,sqlite_table,engine

def load_json():
	sqlite_connection,sqlite_table,engine=sqlengine()
	df = pd.read_sql_table(sqlite_table, engine)
	js = df.to_json(orient = 'records')
	return js

def load_table():
	sqlite_connection,sqlite_table,engine=sqlengine()
	df = pd.read_sql_table(sqlite_table, engine)
	return df

if __name__ == '__main__':
	process_and_predict()