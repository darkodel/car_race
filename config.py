import json

CONFIG = '.config.json'
CONFIG_PLAYERS = '.config_players.json'

def load_config(config_file_path=CONFIG):
    with open(config_file_path) as config_file:
        data = json.load(config_file)
    
    return(data)

def edit_score_history(data, score_history_path=CONFIG_PLAYERS):
    with open(score_history_path, 'w+') as score_history:
        json.dump(data, score_history)

def create_score_history():
    data = load_config()
    empty_score_history = data['players']
    edit_score_history(empty_score_history)

def remove_player(player_x):
    score_history = load_score_history() # load the whole score history
    for p in score_history['player']:
        if p['name'] == player_x: # find the element (dictionary) in player list contaning player x
            score_history['player'].remove(p) # remove that element (dictionary)
            # If player_x is last_player change it to Anonymous.
            if score_history['last_player'] == player_x:
                score_history['last_player'] = 'Anonymous'
    edit_score_history(score_history) # write it back to the file

def create_new_player(new_player):
    data = load_config()
    new_player_score_history = data['players']['player'] # get player's section
    new_player_score_history[0]['name'] = new_player # insert new player name
    data = load_score_history() # load the whole score history
    data['player'].append(new_player_score_history[0]) # append new player to the player's list
    edit_score_history(data) # write it back to the file

def load_score_history(score_history_path=CONFIG_PLAYERS):
    try:
        with open(score_history_path) as score_history:
            data = json.load(score_history)
    except:
        create_score_history()
        data = load_score_history()
    finally:
        return(data)