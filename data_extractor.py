# Python 3
import http.client, urllib.parse
import json
import pandas as pd
import pickle
from keras.models import load_model
from sqlalchemy import create_engine


def getResponse(offset):
	conn = http.client.HTTPConnection('api.mediastack.com')

	params = urllib.parse.urlencode({
		'access_key': '97bd1533357df03f595417b0d962e28c',
		'languages': 'en',
		'categories': 'technology',
		'limit': 100,
		'offset':offset,
		})

	conn.request('GET', '/v1/news?{}'.format(params))
	res = conn.getresponse()
	return res


def getTotalData(res):
	data = res.read()
	stringData=data.decode('utf-8')
	jsondata = json.loads(stringData)
	total=jsondata['pagination']['total']
	return total

def getTotalOffset(total):
	return int(total/100)

def getAllData(offset):
	print('Page Number:',offset)
	res=getResponse(offset)
	data=res.read()
	stringData=stringData=data.decode('utf-8')
	jsondata = json.loads(stringData)
	data=jsondata['data']
	for i in data:
		newsData.append(i)
        
def getDataFrame(newsData):
	authors=[]
	title=[]
	description=[]
	url=[]
	source=[]
	country=[]
	date=[]
	for i in newsData:
	    authors.append(i['author'])
	    title.append(i['title'])
	    description.append(i['description'])
	    url.append(i['url'])
	    source.append(i['source'])
	    country.append(i['country'])
	    date.append(i['published_at'])
	df=pd.DataFrame({"Author":authors, 'Title':title,"Description":description,'URL':url,'Source':source,'Country':country,'Date':date})
	return df

def get_data():
	connection=getResponse(0)
	total_data=getTotalData(connection)
	pagination_count=getTotalOffset(total_data)
	print("We have ",str(pagination_count)," pages of data. Please wait while we load them all.")
	for i in range(1,pagination_count+1):
	    getAllData(i)
	df=getDataFrame(newsData)
	save_database(df)

def sqlengine():
	engine = create_engine('sqlite:///news_data.db', echo=True)
	sqlite_connection = engine.connect()
	sqlite_table = "News"
	return sqlite_connection,sqlite_table,engine

def save_database(df):
	sqlite_connection,sqlite_table,engine = sqlengine()
	df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')

def viewData():
	sqlite_connection,table_name,engine = sqlengine()
	df = pd.read_sql_table(table_name, engine)
	js = df.to_json(orient = 'records')
	return js