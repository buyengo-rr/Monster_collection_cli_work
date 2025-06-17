type_chart = {
    'Fire':     {'Grass': 2.0, 'Water': 0.5, 'Electric': 1.0, 'Fire': 0.5},
    'Water':    {'Fire': 2.0, 'Grass': 0.5, 'Electric': 1.0, 'Water': 0.5},
    'Grass':    {'Water': 2.0, 'Fire': 0.5, 'Electric': 1.0, 'Grass': 0.5},
    'Electric': {'Water': 2.0, 'Grass': 0.5, 'Fire': 1.0, 'Electric': 0.5},
}

def get_effectiveness(attacker_type, defender_type):
    return type_chart.get(attacker_type, {}).get(defender_type, 1.0)
