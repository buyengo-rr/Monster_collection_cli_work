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
def main_menu(player_id):
    while True:
        print("\n📜 Main Menu:")
        print("1. 🗺️ Explore (Catch monsters)")
        print("2. 📦 View Collection")
        print("3. ⬆️ Level Up a Monster")
        print("4. 💊 Heal a Monster")
        print("5. ⚔️ Battle Wild Monster")
        print("6. 🚪 Exit")
        choice = input("➡️ ").strip()
        if choice == '1':
            explore(player_id)
        elif choice == '2':
            view_collection(player_id)
        elif choice == '3':
            level_up_prompt(player_id)
        elif choice == '4':
            heal_monster_prompt(player_id)
        elif choice == '5':
            battle_wild_monster(player_id)
        elif choice == '6':
            print("👋 Goodbye, Trainer!")
            break
        else:
            print("❌ Invalid option.")

def explore(player_id):
    session = get_session()
    species_list = session.query(MonsterSpecies).all()
    wild_mon = random.choice(species_list)
    print(f"🌲 You encounter a wild {wild_mon.name} ({wild_mon.type}, Rarity: {wild_mon.rarity:.2f})!")
    attempt = input("🎯 Attempt to catch? (y/n): ").lower()
    if attempt == 'y':
        success = catch_monster(player_id, wild_mon.id)
        if success:
            print(f"✅ Success! {wild_mon.name} joined your team!")
            nickname_monster_prompt(player_id, wild_mon.id)
        else:
            print("💨 Oh no! The monster escaped!")
    else:
        print("❎ You decided not to catch it.")
    session.close()

def view_collection(player_id):
    monsters = get_player_collection(player_id)
    if not monsters:
        print("📭 Your collection is empty.")
        return
    print(f"\n📚 Your Monsters:")
    for i, mon in enumerate(monsters, 1):
        nick = mon.nickname if mon.nickname else mon.species.name
        print(f"{i}. 🧬 {nick} (Lv. {mon.level}) ❤️ {mon.current_hp}/{mon.max_hp}")
def level_up_prompt(player_id):
    monsters = get_player_collection(player_id)
    if not monsters:
        print("📉 You have no monsters to level up.")
        return
    print("🔼 Choose a monster to level up:")
    for i, mon in enumerate(monsters, 1):
        nick = mon.nickname if mon.nickname else mon.species.name
        print(f"{i}. {nick} (Lv. {mon.level})")
    choice = input("➡️ ")
    try:
        idx = int(choice) - 1
        monster = monsters[idx]
        new_stats = level_up_monster(monster.id)
        print(f"💪 {monster.species.name} is now level {new_stats['level']}!")
    except Exception:
        print("❌ Invalid choice.")


