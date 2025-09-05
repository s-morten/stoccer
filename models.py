from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = "USERS"
    __table_args__ = {'schema': 'STOCCER'}

    user_id = Column(Integer, primary_key=True, index=True)

class Portfolio_items(Base):
    __tablename__ = "PORTFOLIO_ITEMS"
    __table_args__ = {'schema': 'STOCCER'}

    user_id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer)

class Dim_stocks(Base):
    __tablename__ = "DIM_STOCKS"
    __table_args__ = {'schema': 'STOCCER'}

    stock_id = Column(Integer, primary_key=True, index=True)

class Fak_stocks(Base):
    __tablename__ = "FAK_STOCKS"
    __table_args__ = {'schema': 'STOCCER'}

    stock_id = Column(Integer, primary_key=True, index=True)
    valid_from = Column(Date)
    valid_to = Column(Date)
    price = Column(Float)