import os
import sys 
from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine 

Base = declarative_base()

class User(Base): 
	__tablename__ = 'user'
	#Table to maintain usernames and passwords
	username = Column(String(250), primary_key = True)
	password = Column(String(250))

class Balance(Base): 
	__tablename__ = 'balance'
	username = Column(String(250), ForeignKey("user.username"), primary_key = True)
	trading_balance = Column(Integer)
	checking_balance = Column(Integer)
	user = relationship(User)

engine = create_engine('sqlite:///sqlalchemy_user.db')

Base.metadata.create_all(engine)



