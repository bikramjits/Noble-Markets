from models import User, Base, Balance 
from sqlalchemy import create_engine 

engine = create_engine('sqlite:///sqlalchemy_user.db')

Base.metadata.bind = engine 

from sqlalchemy.orm import sessionmaker 

DBSession = sessionmaker()
DBSession.bind = engine 

session = DBSession()

session.query(User).all()
# [<models.Balance object at 0x2ee3cd0>]

person = session.query(User).first()

person.username 

lalala = session.query(User).filter(User.username == "lalalal").first()
# [<models.Balance object at 0x2ee3cd0>]

session.query(Balance).filter(Balance.user == person).one()


print(person.username)
print(person.password)

print(lalala.username)