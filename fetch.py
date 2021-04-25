import requests
from dotenv import load_dotenv
import os
import time

from sqlalchemy.orm import Session
from models import *

load_dotenv()

def fetch_data(engine): 
	session=Session(engine)
	api_url='http://api.511.org/traffic/events?'
	FIVEONEONE_TOKEN=os.getenv('FIVEONEONE_TOKEN')
	query_params={
		'api_key': FIVEONEONE_TOKEN, 
		'format': 'json'
		}
	response=requests.get(api_url, params=query_params)
	if str(response.status_code)[0]=='2':
		response.encoding='utf-8-sig'
		events_list=response.json()['events']
		for each_event in events_list: 
			new_event={
				'event_id': each_event['id'], 
				'time': time.time(), 
				'headline': each_event['headline'], 
				'event_type': each_event['event_type'], 
				'severity': each_event['severity'], 
				'lat': each_event['geography']['coordinates'][1], 
				'lon': each_event['geography']['coordinates'][0]
				}
			session.add(Events(**new_event)) # Event(event_id=event_id, time=time, headline=headline, etc)
		session.commit()
		print(f'SUCCESS')
	else: 
		print('FAILED')
	session.close()
	return None

#####COMMENT OUT IF USING SCHEDULER#####
# from sqlalchemy import create_engine
# SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or "sqlite:///db.sqlite"
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Base.metadata.create_all(engine)
# fetch_data(engine)
########################################
