# Monster Collection & Battle Game

A simple monster collection and battle game, inspired by classic creature-collecting games.  
Players can catch monsters, train them, level them up, and battle against other creatures using abilities with type effectiveness.

## Features

- Collect unique monsters with different stats, types, and abilities
- Turn-based battle system with type effectiveness
- Level up your monsters to increase their stats
- Simple catching mechanics with rarity-based chance
- SQLite database backend with SQLAlchemy ORM
- Modular and easy to expand with new monsters, abilities, and types

## Technologies Used

- Python 3.x
- SQLAlchemy (ORM)
- SQLite
- Modular code structure for game logic and models

## How to Run

1. Clone the repository:

    ```bash
    git clone <your-repo-url>
    cd <repo-folder>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Seed the monster species database:

    ```bash
    python seeds/seed_species.py
    ```

4. Start playing by running your game logic (you can build a CLI or GUI interface)

## Project Structure

.
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── __pycache__
│   ├── battle.cpython-311.pyc
│   └── game_engine.cpython-311.pyc
├── battle.py
├── cli.py
├── game_engine.py
├── models
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── base.cpython-311.pyc
│   │   ├── monster_species.cpython-311.pyc
│   │   ├── player.cpython-311.pyc
│   │   └── player_monster.cpython-311.pyc
│   ├── base.py
│   ├── monster_species.py
│   ├── player.py
│   └── player_monster.py
├── monster_collection.db
├── seeds
│   ├── __pycache__
│   │   └── seed_monster_species.cpython-311.pyc
│   └── seed_monster_species.py
└── utils
    ├── __pycache__
    │   └── type_effectiveness.cpython-311.pyc
    └── type_effectiveness.py

8 directories, 24 files


## Creators

- **Diagne**
- **Patrick**

---

Happy collecting & battling! 🚀
