from apscheduler.schedulers.blocking import BlockingScheduler
import fetch
from sqlalchemy import create_engine
from models import *
import os

sched=BlockingScheduler()
fetch_freq_mins=1

SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or "sqlite:///db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)

@sched.scheduled_job('interval', minutes=fetch_freq_mins)
def minute_job(): 
	fetch.fetch_data(engine)
	# This job is run every {fetch_freq_mins} minutes
	return None

sched.start()