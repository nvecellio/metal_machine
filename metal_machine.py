import json

with open('secret.txt', 'r') as conf_file:
    conf = json.load(conf_file)

CLIENT_ID = conf['client_id']
CLIENT_SECRECT = conf['client_secret']
