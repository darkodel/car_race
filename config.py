import json

def load_config(config_file_path='config.json'):
    with open(config_file_path) as config_file:
        data = json.load(config_file)
    
    return(data)

def load_score_history(score_history_path='players.json'):
    with open(score_history_path) as score_history:
        data = json.load(score_history)

    return(data)

def edit_score_history(data, score_history_path='players.json'):
    with open(score_history_path, 'w+') as score_history:
        json.dump(data, score_history)

""" data = load_config()

print(data)
print(data['display_caption'])
print(data['players'])
print(data['players']['player'][0])
print(data['players']['player'][1])

for player in data['players']:
    print(player) """

data = load_score_history()

print(data)
