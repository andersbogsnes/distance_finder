from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float, ForeignKey, Boolean
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
        return session.query(cls).filter(cls.address == address).first()

    @classmethod
    def create_address(cls, client, session, address, home_office):
        lat, lng = get_lat_long(client, address)
        new_address = cls(address=address, lat=lat, long=lng, home_office=home_office)
        session.add(new_address)
        session.commit()
        return new_address

    def haversine_distance(self, other: 'Address'):
        if not isinstance(other, Address):
            raise DistanceAPIError(f"Must compare to another Address - got {type(other)}")
        return haversine(self.long, self.lat, other.long, other.lat)


class Distance(Base):
    __tablename__ = 'distance'

    id = Column(Integer, primary_key=True)
    from_address = Column(Integer, ForeignKey('address.id'))
    to_address = Column(Integer, ForeignKey('address.id'))
    distance = Column(Integer)
