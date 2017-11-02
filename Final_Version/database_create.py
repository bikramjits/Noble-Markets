"""

The Following Code inserts values in tables created by models.py. 

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import Balance, Base, User

engine = create_engine('sqlite:///sqlalchemy_user.db')

Base.metadata.bind = engine 

DBSession = sessionmaker(bind = engine)

session = DBSession()

new_user = User(username = "Jack", password= "jack")
session.add(new_user)
session.commit()

new_balance = Balance(username = "Jack", trading_balance = 700, checking_balance = 800, user = new_user)
session.add(new_balance)
session.commit()

new_user = User(username = "Jill", password= "jill")
session.add(new_user)
session.commit()

new_balance = Balance(username = "Jill", trading_balance = 800, checking_balance = 700, user = new_user)
session.add(new_balance)
session.commit()

