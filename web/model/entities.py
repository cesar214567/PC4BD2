from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from database import connector

class image(connector.Manager.Base):
    __tablename__='image'
    id = Column(String(22),primary_key=True)
    nombre = Column(String(30))
        
