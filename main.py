import requests
import os
from requests.auth import HTTPBasicAuth
import sqlite3
import json
from ColumnReferences import *

master_list = []


def make_card_info_list(entry):
    temp_pkmn_dict = pkmn_dict.copy()
    for key, value in entry.items():
        if key in temp_pkmn_dict.keys():
            temp_pkmn_dict[key] = value
    master_list.append(temp_pkmn_dict)


def make_row_from_master(master_row):
    vals_as_list = list(master_row.values())
    for index in range(len(vals_as_list)):
        print(vals_as_list[index])


def convert_energy_list(energy_list):
    final_string = ''
    energy_list_as_set = set(energy_list)
    for item in energy_list_as_set:
        final_string += item + '_' + str(energy_list.count(item)) + ' '
    return final_string


def extract_attack(attack_dict):
    attack_dict_cpy = attack_dict.copy()
    if len(attack_dict_cpy['cost']) > 0:
        attack_dict_cpy['cost'] = convert_energy_list(attack_dict_cpy['cost'])
    return attack_dict_cpy


def format_for_db_insertion(pkmn_row):
    temp_row_dict = overview_key_list.copy()
    for k, v in pkmn_row.items():
        temp_row_dict[k] = v
    return '(' + ','.join(temp_row_dict.values()) + ')'


# ----------------------- API ---------------------- #

method = "get"
api_key = os.environ.get("API_KEY")
endpoint = "https://api.pokemontcg.io/v2/cards"
auth = HTTPBasicAuth('apikey', api_key)

parameters = {
    'orderBy': 'set',
    'page': '1'
}

response = requests.get(url=endpoint, auth=auth, params=parameters)
response.raise_for_status()
all_cards_page_1 = response.json()
all_data_page_1 = all_cards_page_1['data']
#print(all_data_page_1)
for i in all_data_page_1:
    make_card_info_list(i)

parameters['page'] = '2'
response = requests.get(url=endpoint, auth=auth, params=parameters)
response.raise_for_status()
all_cards_page_2 = response.json()
all_data_page_2 = [i for i in all_cards_page_2['data'] if i['set']['name'] != 'Team Rocket' and
                   i['set']['name'] != 'Legendary Collection']
for i in all_data_page_2:
    make_card_info_list(i)

attacks_list = []
for pkmn in master_list:
    if len(pkmn['subtypes']) > 0:
        pkmn['subtypes'] = pkmn['subtypes'][0]
    if len(pkmn['types']) > 0:
        pkmn['types'] = pkmn['types'][0]
    if len(pkmn['evolvesTo']) > 0:
        pkmn['evolvesTo'] = pkmn['evolvesTo'][0]
    if len(pkmn['weaknesses']) > 0:
        pkmn['weaknesses'] = pkmn['weaknesses'][0]['type']
    if len(pkmn['resistances']) > 0:
        pkmn['resistances'] = pkmn['resistances'][0]['type']
    if len(pkmn['retreatCost']) > 0:
        pkmn['retreatCost'] = convert_energy_list(pkmn['retreatCost'])

    if len(pkmn['attacks']) > 0:

        for attack_data in pkmn['attacks']:
            duplicate_attack = False

            for count, extracted_attack in enumerate(attacks_list, 1):
                pkmn[f'attack{count}'] = attack_data['name']

                if extracted_attack['name'] == attack_data['name']:
                    duplicate_attack = True
                    break

            if not duplicate_attack:
                attacks_list.append(extract_attack(attack_data))

    pkmn.pop('attacks')

print(format_for_db_insertion(master_list[0]))
# for r in master_list:
#     make_row_from_master(r)
#     print('----------------------------\n')
# master_json = json.dumps(master_list, indent=4).replace(r'\u00e9', 'e')



# -------------------------- SQL --------------------------#

connection = sqlite3.connect('PkmnCards.db')
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()

overview_columns = ','.join(db_overview_col_list)
attack_table_columns = ','.join(db_attacks_col_list)

cursor.execute(f"CREATE TABLE iF NOT EXISTS CardsOverview({overview_columns})")
cursor.execute(f"CREATE TABLE iF NOT EXISTS AttacksTable({attack_table_columns})")

entire_formatted_master = """"""
for pkmn_row in master_list:
    entire_formatted_master += format_for_db_insertion(pkmn_row) + ','



# result = cursor.execute("SELECT name FROM sqlite_master")
