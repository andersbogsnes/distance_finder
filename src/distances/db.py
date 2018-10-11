from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from .utils import haversine, DistanceAPIError

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    lat = Column(Float)
    long = Column(Float)

    @classmethod
    def address_exists(cls, session, address):
        return session.query(cls).filter(cls.address == address).first()

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
