pkmn_dict = {
    'id': '',
    'name': '',
    'supertype': '',
    'subtypes': '',
    'level': '',
    'hp': '',
    'types': '',
    'evolvesFrom': '',
    'evolvesTo': '',
    'attacks': '',
    'weaknesses': '',
    'resistances': '',
    'retreatCost': ''
}

overview_key_list = {
    'id': '',
    'name': '',
    'supertype': '',
    'subtypes': '',
    'level': '',
    'hp': '',
    'types': '',
    'evolvesFrom': '',
    'evolvesTo': '',
    'attack1': '',
    'attack2': '',
    'weaknesses': '',
    'resistances': '',
    'retreatCost': ''
}


db_overview_col_list = [
    'id TEXT PRIMARY KEY',
    'name TEXT',
    'supertype TEXT',
    'subtypes TEXT',
    'level INTEGER',
    'hp INTEGER',
    'types TEXT',
    'evolvesFrom TEXT',
    'evolvesTo TEXT',
    'attack1 TEXT',
    'attack2 TEXT',
    'weaknesses TEXT',
    'resistances TEXT',
    'retreatCost TEXT',
    'FOREIGN KEY (attack1) REFERENCES AttacksTable(name)',
    'FOREIGN KEY (attack2) REFERENCES AttacksTable(name)'
]

db_attacks_col_list = [
    'name TEXT PRIMARY KEY',
    'cost TEXT',
    'damage INTEGER',
    'text TEXT'
]
