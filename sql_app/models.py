from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

#Create the database models
class User(Base):
	"""docstring for User"""
	__tablename__ = "users"

	#Create model attributes/columns
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	hashed_password = Column(String)
	is_active = Column(Boolean, default=True)

	#Create the relationships
	items = relationship("Item", back_populates="owners")

class Item(Base):
	"""docstring for Item"""
	__tablename__ = "items"

	#Create model attributes/columns
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String, index=True)
	owner_id = Column(Integer, ForeignKey("users.id"))

	#Create the relationships
	owner = relationship("User", back_populates="items")
