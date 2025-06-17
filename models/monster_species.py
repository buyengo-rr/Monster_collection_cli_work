from sqlalchemy import Column, Integer, String, JSON, Float
from .base import Base

class MonsterSpecies(Base):
    __tablename__ = 'monster_species'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    base_stats = Column(JSON, nullable=False)
    rarity = Column(Float, nullable=False)
    abilities = Column(JSON, nullable=False)
