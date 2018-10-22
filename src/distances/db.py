from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship

from .utils import haversine, DistanceAPIError
from .geocoding import get_lat_long

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    lat = Column(Float)
    long = Column(Float)
    home_office = Column(Boolean)

    def __init__(self, address, home_office, lat=None, long=None):
        self.address = address
        self.lat = lat
        self.long = long
        self.home_office = home_office

    @classmethod
    def get_address(cls, session, address):
        return session.query(cls).filter(cls.address == address).one_or_none()

    @classmethod
    def create_address(cls, session, address, home_office):
        lat, lng = get_lat_long(address)
        new_address = cls(address=address,
                          lat=lat,
                          long=lng,
                          home_office=home_office)
        session.add(new_address)
        session.commit()
        return new_address

    @classmethod
    def get_addresses(cls, session: 'Session', addresses: List[str]):
        return session.query(cls).filter(cls.address.in_(addresses)).all()


class Distance(Base):
    __tablename__ = 'distance'

    id = Column(Integer, primary_key=True)
    from_address_id = Column(Integer, ForeignKey('address.id'))
    to_address_id = Column(Integer, ForeignKey('address.id'))
    distance = Column(Integer)
    duration = Column(Integer)

    from_address = relationship("Address", primaryjoin=from_address_id == Address.id,
                                backref='from_distance')
    to_address = relationship("Address", primaryjoin=to_address_id == Address.id,
                              backref='to_distance')

    def __init__(self, from_address_id, to_address_id, distance, duration):
        self.from_address_id = from_address_id
        self.to_address_id = to_address_id
        self.distance = distance
        self.duration = duration

    @classmethod
    def create_distance(cls,
                        from_address: 'Address',
                        to_address: 'Address',
                        distance: int,
                        duration: int,
                        session: 'Session'):
        new_distance = cls(from_address.id, to_address.id, distance, duration)
        session.add(new_distance)
        session.commit()
        return new_distance

    @classmethod
    def get_distance(cls, session: 'Session', from_address: 'Address', to_address: 'Address'):
        return session.query(cls).filter(cls.from_address_id == from_address.id,
                                         cls.to_address_id == to_address.id).one_or_none()
