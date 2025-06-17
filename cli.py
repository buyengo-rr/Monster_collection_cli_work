import sys
import random
from models.base import Base, engine, get_session
from models.player import Player
from models.monster_species import MonsterSpecies
from models.player_monster import PlayerMonster
from game_engine import catch_monster, get_player_collection, level_up_monster
from seeds.seed_monster_species import seed_species
from sqlalchemy.orm import sessionmaker

def start_game():
    print("🧟 Welcome to ⚔️ Monster Collector!")

    Base.metadata.create_all(bind=engine)
    seed_species()

    Session = sessionmaker(bind=engine)
    session = Session()

    username = input("👤 Enter your username to start or load your game: ").strip()
    player = session.query(Player).filter_by(username=username).first()
    
    if not player:
        player = Player(username=username)
        session.add(player)
        session.commit()
        print(f"🆕 New player '{username}' created!")

    print(f"🙋 Hello, {player.username}! Your level: {player.level}")
    print("🐣 Choose your starter monster:")

    species_list = session.query(MonsterSpecies).filter(MonsterSpecies.rarity < 0.2).all()
    for i, mon in enumerate(species_list[:3], 1):
        print(f"{i}. {mon.name} ({mon.type}) - ❤️ HP: {mon.base_stats['hp']}")

    choice = input("👉 Pick 1, 2 or 3: ")
    try:
        idx = int(choice) - 1
        starter = species_list[idx]
        already_has = session.query(PlayerMonster).filter_by(player_id=player.id, species_id=starter.id).first()
        if not already_has:
            caught = catch_monster(player.id, starter.id)
            if caught:
                print(f"🎉 {starter.name} joined your team!")
                nickname_monster_prompt(player.id, starter.id)
    except Exception:
        print("❌ Invalid choice.")

    player_id = player.id
    session.commit()
    session.close()
    main_menu(player_id)


