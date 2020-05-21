from sqlite_ex import Base, Device
from sqlalchemy import create_engine
import json

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

device = session.query(Device).all()

test_list = []

for i in device:
	test_list.append((i.series,i.software_version))

print("\n")
print("\n")
print(test_list)

d = {}

for a,b in test_list:
	d.setdefault(a,[]).append(b)

print(d)

y = json.dumps(d)
print("\n")
print(y)
#test_dic = {}
