from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float

Base = declarative_base()


class Address(Base):
    __tablename__ = 'adress'

    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    lat = Column(Float)
    long = Column(Float)

    @classmethod
    def address_exists(cls, session, address):
        return session.query(cls).where(cls.address == address).first()


class Distance(Base):
    __tablename__ = 'distance'

    address_from = Column(Integer, )
