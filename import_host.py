import json
import sqlite3
configs = json.load(open('config.json'))
db_file_name=configs['servers_remaining']
servers_manual=configs['servers_manual']

## import the public IPs listed in the servers.manual.txt into servers.remaining.db to deploy
with open(servers_manual) as f, sqlite3.connect(db_file_name) as conn:
    lines = f.readlines()
    conn.execute('CREATE TABLE IF NOT EXISTS server(host text)')
    for line in lines:
        conn.execute('INSERT INTO server VALUES ( :host )', { "host": line.strip() })
    print("#################### Hosts have been imported to sqlite database to reploy! ####################")

