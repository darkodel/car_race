import json

def load_config(config_file_path='config.json'):
    with open(config_file_path) as config_file:
        data = json.load(config_file)
    
    return(data)

def edit_score_history(data, score_history_path='.players.json'):
    with open(score_history_path, 'w+') as score_history:
        json.dump(data, score_history)
        
def create_score_history():
    data = load_config()
    empty_score_history = data['players']
    edit_score_history(empty_score_history)

def load_score_history(score_history_path='.players.json'):
    try:
        with open(score_history_path) as score_history:
            data = json.load(score_history)

    except:
        create_score_history()
        data = load_score_history()

    finally:
        return(data)
