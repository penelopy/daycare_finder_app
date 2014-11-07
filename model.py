from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Datetime, Text
from sqlalchemy.orm import sessionmaker, relationship, backref

ENGINE = None
Session = None

Base = declarative_base()

class Parent(Base): 
	__tablename__ = "parents"

	id = Column(Integer, primary_key = True)
	first_name = Column(String(32), nullable = False)
	last_name = Column(String(32), nullable = False)
	username = Column(String(64), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(32), nullable = False)
	zipcode = Column(String(15))
	neighborhood = Column(String(32))

class Center(Base):    
	__tablename__ = "centers"    
	#login info
	id = Column(Integer, primary_key = True)
	username = Column(String(32), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(32), nullable = False)
	#contact info
	biz_name = Column(String(64))
	primary_contact = Column(String(64))
	zipcode = Column(String(15))
	neighborhood = Column(String(32))
	address = Column(String(128))
	phone = Column(String(32))
	web_url = Column(String(64))
	fb_url = Column(String(64))
	# biz facts
	yr_in_biz = Column(Integer(12))
	capacity = Column(String(12))
	num_staff = Column(String(12))
	license_num = Column(String(12))
	current_openings = Column(Boolean)
	special_needs = Column(Boolean) #over simplified could be expanded
	opening_time = Column(Datetime) #FIXME adjust for just time?
	closing_time = Column(Datetime)	#FIXME adjust for just time?
	type_of_center_id = Column(Integer, ForeignKey('type_of_center.id')) 
	rate = Column(Text)
	# contextual details
	about_us = Column(Text)
	philosophy = Column(Text)
	activities = Column(Text)

	type_of_center = relationship("Type", backref="centers")

class Type(Base): #backref to Daycare
	__tablename__ = "type_of_center"
	id = Column(Integer, primary_key = True)
	name = Column(String(16)) # matches to type.csv  

class Photo(Base):
	__tablename__ = "photos" 
	id = Column(Integer, primary_key = True)
	center_id = Column(Integer, ForeignKey('centers.id'))
	photo_link = Column(String(100))

	center = relationship("Center", backref="photos")

class Schedule(Base): # has association table (center_schedule)
	__tablename__ = "schedules"
	id = Column(Integer, primary_key = True)
	name = Column(String(16)) #matches to schedule.csv    


center_schedule = Table('center_schedule', Base.metadata, 
	Column('center_schedule_id', Integer, primary_key=True), 
	Column('center_id', Integer, ForeignKey('centers.id')),
	Column('schedule_id', Integer, ForeignKey('schedules.id'))
	 )

class Language(Base): # has association table (center_language)
	__tablename__ = "languages"
	id = Column(Integer, primary_key = True)
	name = Column(String(16)) # matches to languages.csv


center_language = Table('center_language', Base.metadata, 
	Column('center_language_id', Integer, primary_key=True), 
	Column('center_id', Integer, ForeignKey('centers.id')),
	Column('language_id', Integer, ForeignKey('languages.id'))
	 )

class Endorsement(Base):
	__tablename__ = "endorsement"
	id = Column(Integer, primary_key = True)
	daycare_id = Column(Integer, ForeignKey('centers.id'))	
	parent_id = Column(Integer, ForeignKey('parents.id'))
	endorsement = Column(Text)

	center = relationship("Center", backref="endorsements")
	parent = relationship("Parent", backref="endorsements")


upvotes = Table('upvotes', Base.metadata, 
	Column('upvote_id', Integer, primary_key=True), 
	Column('center_id', Integer, ForeignKey('centers.id')),
	Column('parent_id', Integer, ForeignKey('parents.id'))
	 )


class WorksheetRow(Base):    
	__tablename__ = "worksheet_row"
	id = Column(Integer, primary_key = True)
	daycare_id = Column(Integer, ForeignKey('center.id'))	
	parent_id = Column(Integer, ForeignKey('parent.id'))
	notes = Column(Text)
	level_of_interest = Column(String(16))
	last_contacted = Column(Datetime)
	following = Column(Boolean)

	daycare = relationship("Center", backref=backref("worksheets"))
	parent = relationship("Parent", backref=("worksheets"))

def connect(): 
	global ENGINE
	global Session

	ENGINE = create_engine("sqlite:///daycare_finder.db", echo=True)
	Session = sessionmaker(bind=ENGINE)

	return Session()

db_session = connect()

# def create_tables():
#     engine = create_engine("sqlite:///daycare_finder.db", echo=True)
#     Base.metadata.create_all(engine)



def main():
    pass

if __name__ == "__main__":
    main()

