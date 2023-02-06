from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://arch_user:arch_password@127.0.0.1:3360/archdb", echo = True)
conn = engine.connect() 

Base = declarative_base()

class Author(Base):
   __tablename__ = 'Author'
   id = Column(Integer,primary_key=True, index=True)
   first_name = Column(String)
   last_name = Column(String)
   email = Column(String)
   title = Column(String)
   birth_date = Column(Date) 

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)

session = Session()
#c1 = User(name = 'Ravi Kumar', address = 'Station Road Nanded', email = 'ravi@gmail.com')
#session.add(c1)
#session.commit()

#session.add_all([
#   User(name = 'Komal Pande', address = 'Koti, Hyderabad', email = 'komal@gmail.com'), 
#   User(name = 'Rajender Nath', address = 'Sector 40, Gurgaon', email = 'nath@gmail.com'), 
#   User(name = 'S.M.Krishna', address = 'Budhwar Peth, Pune', email = 'smk@gmail.com')]
#)

#session.commit()

#print(f'count: {session.query(Author).count()}')
#result = session.query(User).all()
result = session.query(Author).filter((Author.first_name=='Josh') | (Author.last_name=='Richardson'))

for row in result:
   print ("First name: ",row.first_name, "Last name:", row.last_name, "Title:",row.title, "Email:",row.email)

session.query(Author).\
   filter((Author.first_name=='Josh') & (Author.last_name=='Richardson')).\
      update({'title': 'mister'})

session.commit()

print()
for row in session.query(Author).\
   filter((Author.first_name=='Josh') & (Author.last_name=='Richardson')):
   print ("First name: ",row.first_name, "Last name:", row.last_name, "Title:",row.title, "Email:",row.email)

#session.delete(user)
#session.commit()

