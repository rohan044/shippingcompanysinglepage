from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite_ex import Base, Device

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#new_device = Device(series='DX70_DX80',software_version = 's52040ce9_7_2-3f94b3cda3f.pkg')
#ew_device = Device(series='Spark_Series',software_version = 'cmterm-s53200ce9_5_1-be5deaf82e6.k3.cop.sgn')
#session.add(new_device)
device = session.query(Device).all()
for i in device:
	print(i.id)
	print(i.series)
	print(i.software_version)
#session.commit()



