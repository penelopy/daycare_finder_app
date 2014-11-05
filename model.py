from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

# ENGINE = create_engine("sqlite:///daycare_finder.db", echo=False)
# session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))
Base = declarative_base()
# Base.query = session.query_property()
# Base = declarative_base()

class Daycare(Base):
	__tablename__ = "daycares"

	id = Column(Integer, primary_key = True)
	username = Column(String(32), nullable = False)
	password = Column(String(32), nullable = False)
	biz_name = Column(String(64), nullable = False)
	primary_contact = Column(String(64), nullable = False)
	zipcode = Column(String(15), nullable = False)
	neighborhood = Column(String(32), nullable = False)
	address = Column(String(128), nullable = True)
	phone = Column(String(32), nullable = True) 
	email = Column(String(64), nullable = False)

	web_url = Column(String(64), nullable = True)
	fb_url = Column(String(64), nullable = True)

	yr_in_biz = Column(String(12), nullable = True) # ?? standard practice on data length? 
	capacity = Column(String(12), nullable = True)
	num_staff = Column(String(12), nullable = True)
	license_num = Column(String(12), nullable = True)

	about_us = Column(String(128), nullable = True) # FIXME - should probably allow longer string

	def create_photo_gallery(): #placeholder for creating daycare photo gallery	
		pass

	def create_recommendations(): #placeholder for parent recommendations
		pass



class Parent(Base): 
	__tablename__ = "parents"

	id = Column(Integer, primary_key = True)
	username = Column(String(64), nullable = False)
	password = Column(String(32), nullable = False)
	zipcode = Column(String(15), nullable = False)
	neighborhood = Column(String(32), nullable = False)
	age_of_child_1 = Column(String(12), nullable = True)
	age_of_child_2 = Column(String(12), nullable = True)
	age_of_child_3 = Column(String(12), nullable = True)

	#TODO - create way to upload photo...

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
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()

