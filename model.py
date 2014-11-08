from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Table
from sqlalchemy.orm import sessionmaker, relationship, backref

ENGINE = None
Session = None

Base = declarative_base()

class Parent(Base): 
	__tablename__ = "parents"

	id = Column(Integer, primary_key = True, nullable=False)
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
	id = Column(Integer, primary_key = True, nullable=False)
	username = Column(String(32), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(32), nullable = False)
	#contact info
	biz_name = Column(String(64), nullable=False)
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
	opening_time = Column(String(12))
	closing_time = Column(String(12))
	type_of_center_id = Column(Integer, ForeignKey('types_of_centers.id')) 
	rate = Column(Text)
	# contextual details
	about_us = Column(Text)
	philosophy = Column(Text)
	activities = Column(Text)

	type_of_center = relationship("Type", backref="centers")

class Type(Base): #backref to Daycare
	__tablename__ = "types_of_centers"
	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(16), nullable=False) # matches to type.csv  

class Photo(Base):
	__tablename__ = "photos" 
	id = Column(Integer, primary_key = True, nullable=False)
	center_id = Column(Integer, ForeignKey('centers.id'), nullable=False)
	photo_link = Column(String(100), nullable=False)

	center = relationship("Center", backref="photos")

class Schedule(Base): # has association table (center_schedule)
	__tablename__ = "schedules"
	id = Column(Integer, primary_key = True, nullable=False)
	name = Column(String(16), nullable=False) #matches to schedule.csv    


centers_schedules = Table('centers_schedules', Base.metadata, 
	Column('center_schedule_id', Integer, primary_key=True, nullable=False), 
	Column('center_id', Integer, ForeignKey('centers.id'), nullable=False),
	Column('schedule_id', Integer, ForeignKey('schedules.id'), nullable=False)
	 )

class Language(Base): # has association table (center_language)
	__tablename__ = "languages"
	id = Column(Integer, primary_key = True, nullable=False)
	name = Column(String(16), nullable=False) # matches to languages.csv


centers_languages = Table('centers_languages', Base.metadata, 
	Column('center_language_id', Integer, primary_key=True, nullable=False), 
	Column('center_id', Integer, ForeignKey('centers.id'), nullable=False),
	Column('language_id', Integer, ForeignKey('languages.id'), nullable=False)
	 )

class Endorsement(Base):
	__tablename__ = "endorsements"
	id = Column(Integer, primary_key = True, nullable=False)
	daycare_id = Column(Integer, ForeignKey('centers.id'), nullable=False)	
	parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
	endorsement = Column(Text)

	center = relationship("Center", backref="endorsements")
	parent = relationship("Parent", backref="endorsements")


upvotes = Table('upvotes', Base.metadata, 
	Column('upvote_id', Integer, primary_key=True, nullable=False), 
	Column('center_id', Integer, ForeignKey('centers.id'), nullable=False),
	Column('parent_id', Integer, ForeignKey('parents.id'), nullable=False)
	 )

followings = Table('followings', Base.metadata, 
	Column('following_id', Integer, primary_key=True, nullable=False), 
	Column('center_id', Integer, ForeignKey('centers.id'), nullable=False),
	Column('parent_id', Integer, ForeignKey('parents.id'), nullable=False)
	 ) 

class WorksheetRow(Base):    
	__tablename__ = "worksheet_rows"
	id = Column(Integer, primary_key = True, nullable=False)
	daycare_id = Column(Integer, ForeignKey('centers.id'), nullable=False)	
	parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
	notes = Column(Text)
	level_of_interest = Column(String(16))
	last_contacted = Column(DateTime)

	daycare = relationship("Center", backref="worksheets")
	parent = relationship("Parent", backref="worksheets")

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
    connect()
    Base.metadata.create_all(ENGINE)

if __name__ == "__main__":
    main()


