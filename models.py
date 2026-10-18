from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Float,Date
from datetime import date

class Users(Base):

    __tablename__='users'

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String)
    username=Column(String,unique=True)
    hashed_password=Column(String)


class Transactions(Base):

    __tablename__='transactions'


    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income or expense
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False,default=date.today)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    


