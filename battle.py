import random
from utils.type_effectiveness import get_effectiveness

def calculate_damage(attacker, defender, ability):
    base_power = ability.get('power', 10) if isinstance(ability, dict) else 10
    attacker_attack = attacker.attack
    defender_defense = defender.defense
    multiplier = get_effectiveness(attacker.species.type, defender.species.type)
    damage = int(((base_power * (attacker_attack / max(defender_defense, 1))) * multiplier) * (random.uniform(0.85, 1.0)))
    damage = max(1, damage)
    return damage, multiplier

def perform_ability(attacker, defender, ability_name):
    ability = next(
        (
            a for a in attacker.species.abilities
            if (a['name'] if isinstance(a, dict) else a) == ability_name
        ),
        None
    )
    if ability is None:
        ability = {'name': ability_name, 'power': 20}
    damage, multiplier = calculate_damage(attacker, defender, ability)
    defender.current_hp = max(0, defender.current_hp - damage)
    effectiveness_text = ""
    if multiplier > 1:
        effectiveness_text = "It's super effective! 🔥"
    elif multiplier < 1:
        effectiveness_text = "It's not very effective... 😕"
    msg = (
        f"{attacker.nickname or attacker.species.name} used {ability['name'] if isinstance(ability, dict) else ability}! "
        f"It dealt {damage} damage. {effectiveness_text}"
    )
    return msg, damage
