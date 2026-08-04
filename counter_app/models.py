from sqlalchemy import Column, Integer, Text, BigInteger
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ElectroCounters(Base):
    __tablename__ = 'electro_counters'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    client_name = Column(Text, unique=True)
    address = Column(Integer, unique=True)
    transformation_coefficient = Column(Integer)
    energy_indic = Column(BigInteger)
    energy = Column(BigInteger)

    def __repr__(self):
        return f'{self.id} client_name = {self.client_name}, {self.energy} '
