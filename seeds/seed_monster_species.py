from models.base import Base, engine, get_session
from models.monster_species import MonsterSpecies

def seed_species():
    Base.metadata.create_all(bind=engine)
    session = get_session()

    monsters = [
        {'name': 'Flamewyrm', 'type': 'Fire', 'base_stats': {'hp': 45, 'attack': 60, 'defense': 40, 'speed': 50}, 'rarity': 0.1, 'abilities': ['Fire Blast', 'Flame Tail']},
        {'name': 'Aquafin', 'type': 'Water', 'base_stats': {'hp': 50, 'attack': 50, 'defense': 50, 'speed': 40}, 'rarity': 0.15, 'abilities': ['Water Jet', 'Heal']},
        {'name': 'Vinewhip', 'type': 'Grass', 'base_stats': {'hp': 55, 'attack': 55, 'defense': 45, 'speed': 45}, 'rarity': 0.2, 'abilities': ['Vine Lash', 'Photosynthesis']},
        {'name': 'Sparkbolt', 'type': 'Electric', 'base_stats': {'hp': 40, 'attack': 65, 'defense': 35, 'speed': 60}, 'rarity': 0.05, 'abilities': ['Thunder Shock', 'Quick Dash']},
        {'name': 'Rockgrinder', 'type': 'Earth', 'base_stats': {'hp': 60, 'attack': 70, 'defense': 60, 'speed': 30}, 'rarity': 0.07, 'abilities': ['Stone Smash', 'Defense Curl']},
    ]

    for mon in monsters:
        existing = session.query(MonsterSpecies).filter_by(name=mon['name']).first()
        if not existing:
            session.add(MonsterSpecies(**mon))
    session.commit()
    session.close()

if __name__ == '__main__':
    seed_species()
