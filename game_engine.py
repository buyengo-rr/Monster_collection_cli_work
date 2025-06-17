import random
from sqlalchemy.orm import joinedload
from models.base import get_session
from models.player_monster import PlayerMonster
from models.monster_species import MonsterSpecies
from models.player import Player
from battle import perform_ability

def battle_turn(attacker, defender, ability_name):
    msg, damage = perform_ability(attacker, defender, ability_name)
    return msg, damage

def is_monster_fainted(monster):
    return monster.current_hp <= 0

def calculate_catch_rate(rarity, player_level):
    base_rate = max(0.05, 1 - rarity)
    level_modifier = min(1, player_level / 50)
    return base_rate * level_modifier

def catch_monster(player_id, species_id):
    session = get_session()
    player = session.query(Player).get(player_id)
    species = session.query(MonsterSpecies).get(species_id)
    if not player or not species:
        session.close()
        return False
    chance = calculate_catch_rate(species.rarity, player.level)
    if random.random() <= chance:
        base = species.base_stats
        monster = PlayerMonster(
            player_id=player_id,
            species_id=species_id,
            level=1,
            experience=0,
            max_hp=base['hp'],
            current_hp=base['hp'],
            attack=base['attack'],
            defense=base['defense'],
            speed=base['speed'],
        )
        session.add(monster)
        session.commit()
        session.close()
        return True
    session.close()
    return False

def get_player_collection(player_id):
    session = get_session()
    monsters = session.query(PlayerMonster).options(joinedload(PlayerMonster.species))\
                     .filter_by(player_id=player_id).all()
    session.close()
    return monsters

def level_up_monster(monster_id):
    session = get_session()
    monster = session.query(PlayerMonster).get(monster_id)
    if not monster:
        session.close()
        return {}
    monster.level += 1
    species = monster.species
    monster.max_hp = int(species.base_stats['hp'] * (1 + 0.1 * (monster.level - 1)))
    monster.current_hp = monster.max_hp
    monster.attack = int(species.base_stats['attack'] * (1 + 0.1 * (monster.level - 1)))
    monster.defense = int(species.base_stats['defense'] * (1 + 0.1 * (monster.level - 1)))
    monster.speed = int(species.base_stats['speed'] * (1 + 0.1 * (monster.level - 1)))
    session.commit()
    data = {
        'level': monster.level,
        'max_hp': monster.max_hp,
        'attack': monster.attack,
        'defense': monster.defense,
        'speed': monster.speed
    }
    session.close()
    return data
