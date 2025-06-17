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
def nickname_monster_prompt(player_id, species_id):
    session = get_session()
    mon = session.query(PlayerMonster)\
        .filter_by(player_id=player_id, species_id=species_id)\
        .order_by(PlayerMonster.id.desc())\
        .first()
    if mon:
        print(f"✨ You caught a {mon.species.name}!")
        nickname = input("📛 Would you like to give it a nickname? (leave empty for none): ").strip()
        if nickname:
            mon.nickname = nickname
            session.commit()
            print(f"✅ Nicknamed your monster '{nickname}'!")
    session.close()
def heal_monster_prompt(player_id):
    monsters = get_player_collection(player_id)
    if not monsters:
        print("💉 You have no monsters to heal.")
        return
    print("💊 Choose a monster to heal:")
    for i, mon in enumerate(monsters, 1):
        nick = mon.nickname if mon.nickname else mon.species.name
        print(f"{i}. {nick} (HP: {mon.current_hp}/{mon.max_hp})")
    choice = input("➡️ ")
    try:
        idx = int(choice) - 1
        monster = monsters[idx]
        if monster.current_hp == monster.max_hp:
            print(f"💡 {monster.nickname or monster.species.name} is already at full health.")
            return
        session = get_session()
        mon_db = session.query(PlayerMonster).get(monster.id)
        mon_db.current_hp = mon_db.max_hp
        session.commit()
        session.close()
        print(f"💖 {monster.nickname or monster.species.name} was fully healed!")
    except Exception:
        print("❌ Invalid choice.")
from battle import perform_ability

def battle_wild_monster(player_id):
    session = get_session()
    player_monsters = get_player_collection(player_id)
    if not player_monsters:
        print("📉 You have no monsters to battle with.")
        session.close()
        return
    
    print("Choose a monster to battle with:")
    for i, mon in enumerate(player_monsters, 1):
        nick = mon.nickname or mon.species.name
        print(f"{i}. {nick} (Lv. {mon.level}) HP: {mon.current_hp}/{mon.max_hp}")

    choice = input("➡️ ")
    try:
        idx = int(choice) - 1
        your_monster = player_monsters[idx]
    except Exception:
        print("❌ Invalid choice.")
        session.close()
        return
    
    wild_monster = random.choice(session.query(MonsterSpecies).all())
    print(f"🌲 A wild {wild_monster.name} appeared!")

    wild = PlayerMonster(
        id=-1,
        player_id=None,
        species_id=wild_monster.id,
        species=wild_monster,
        nickname=None,
        level=1,
        experience=0,
        max_hp=wild_monster.base_stats['hp'],
        current_hp=wild_monster.base_stats['hp'],
        attack=wild_monster.base_stats['attack'],
        defense=wild_monster.base_stats['defense'],
        speed=wild_monster.base_stats['speed'],
    )

    print(f"⚔️ Battle start! {your_monster.nickname or your_monster.species.name} VS Wild {wild.species.name}")

    while your_monster.current_hp > 0 and wild.current_hp > 0:
        print(f"\nYour HP: {your_monster.current_hp}/{your_monster.max_hp}")
        print(f"Wild {wild.species.name} HP: {wild.current_hp}/{wild.max_hp}")

        print("Choose ability to use:")
        for i, ab in enumerate(your_monster.species.abilities, 1):
            ab_name = ab if isinstance(ab, str) else ab['name']
            print(f"{i}. {ab_name}")

        choice = input("➡️ ")
        try:
            ab_idx = int(choice) - 1
            ability = your_monster.species.abilities[ab_idx]
            ability_name = ability if isinstance(ability, str) else ability['name']
        except Exception:
            print("❌ Invalid ability.")
            continue
        
        msg, damage = perform_ability(your_monster, wild, ability_name)
        print(msg)

        if wild.current_hp <= 0:
            print(f"🎉 You defeated the wild {wild.species.name}!")
            break
        
        wild_ability = random.choice(wild.species.abilities)
        wild_ability_name = wild_ability if isinstance(wild_ability, str) else wild_ability['name']
        msg, damage = perform_ability(wild, your_monster, wild_ability_name)
        print(f"Wild {wild.species.name} used {wild_ability_name}!")
        print(msg)

        if your_monster.current_hp <= 0:
            print(f"💀 Your {your_monster.nickname or your_monster.species.name} was defeated!")
            break

    session.close()

if __name__ == '__main__':
    start_game()

