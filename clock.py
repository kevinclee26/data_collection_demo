from apscheduler.schedulers.blocking import BlockingScheduler
import fetch_job
import os

from sqlalchemy import create_engine # imports the methods needed to connect with database
from models import * # import Base and Events class from models.py

sched=BlockingScheduler() # initialize a scheduler that defaults with a job store
fetch_freq_mins=1

SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or "sqlite:///db.sqlite" # use a local sqlite 
																				# database for development
SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://')
engine = create_engine(SQLALCHEMY_DATABASE_URI) # establish connection with database
Base.metadata.create_all(engine) # create all tables associated with the Base; will not attempt to recreate tables

@sched.scheduled_job('interval', minutes=fetch_freq_mins) # decorate function w/ scheduled_job() at specific 'intervals'
def interval_job(): 
	fetch_job.fetch_data(engine) # this job is run every {fetch_freq_mins} minutes
	return None

sched.start() # starting the scheduler is done by simply calling start() on the scheduler