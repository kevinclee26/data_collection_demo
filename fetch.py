import requests
from dotenv import load_dotenv
import os

load_dotenv() # use dotenv to hide sensitive credentials as environment variables

api_url='http://api.511.org/traffic/events?' # base url from 511.org
FIVEONEONE_TOKEN=os.getenv('FIVEONEONE_TOKEN') # retrieve environment variables
query_params={'api_key': FIVEONEONE_TOKEN, 
			  'format': 'json'}
response=requests.get(api_url, params=query_params)
if str(response.status_code)[0]=='2': # check for success
	print('SUCCESS')
else: # output for fail
	print('FAILED')