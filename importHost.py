import json
import sqlite3
configs = json.load(open('config.json'))
dbFileName=configs['servers_remaining']
serversManual=configs['servers_manual']

## import the public IPs listed in the servers.manual.txt into servers.remaining.db to deploy
with open(serversManual) as f, sqlite3.connect(dbFileName) as conn:
    lines = f.readlines()
    conn.execute('CREATE TABLE IF NOT EXISTS server(host text)')
    for line in lines:
        conn.execute('INSERT INTO server VALUES ( :host )', { "host": line.strip() })
    print("#################### Hosts have been imported to sqlite database to reploy! ####################")

