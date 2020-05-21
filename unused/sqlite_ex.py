import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer,primary_key = True)
    series = Column(String(50),nullable = False)
    software_version = Column(String(250),nullable = False)

engine = create_engine('sqlite:///sqlalchemy_example.db')

Base.metadata.create_all(engine)
