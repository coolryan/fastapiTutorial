#SQL (Relational) Databases
##Create the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

#Create the SQLAlchemy engine
engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Create a SessionLocal class
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create a Base class
Base = declarative_base()
