import requests
from dotenv import load_dotenv
import os
import time

from sqlalchemy import create_engine 
from sqlalchemy.orm import Session # imports the methods needed to connect with database
from models import * # import Base and Events class from models.py

load_dotenv() # use dotenv to hide sensitive credentials as environment variables

api_url='http://api.511.org/traffic/events?' # base url from 511.org
FIVEONEONE_TOKEN=os.getenv('FIVEONEONE_TOKEN') # retrieve environment variables
query_params={'api_key': FIVEONEONE_TOKEN, 
			  'format': 'json'}

SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or "sqlite:///db.sqlite" # use a local sqlite 
										# database for development
engine = create_engine(SQLALCHEMY_DATABASE_URI) # establish connection with database
Base.metadata.create_all(engine) # create all tables associated with the Base; will not attempt to recreate tables

session=Session(engine) # the session object is responsible for communicating with the database
response=requests.get(api_url, params=query_params)
if str(response.status_code)[0]=='2':
	response.encoding='utf-8-sig'
	data_list=response.json()['events']
	# iterate through list of records
	for each_event in data_list: 
		# create a Python dictionary with k-v pairs associated with each column
		new_event={'event_id': each_event['id'], 
				   'time': time.time(), 
				   'headline': each_event['headline'], 
				   'event_type': each_event['event_type'], 
				   'severity': each_event['severity'], 
				   'lat': each_event['geography']['coordinates'][1], 
				   'lon': each_event['geography']['coordinates'][0]} # lat/lon are held in nested containers
		# add record
		session.add(Events(**new_event)) # the ** operator allows us to take a dictionary of 
						 # key-value pairs and unpack it into keyword arguments 
						 # in a function call
	session.commit() # commit all changes 
	print('SUCCESS')
else: 
	print('FAILED')
session.close() # close the session
engine.dispose() # close connection pool