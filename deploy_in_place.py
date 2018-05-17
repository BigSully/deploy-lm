import sys, os, json, sqlite3
from task_dispatcher import parallel_run
from action import deploy
import utils;
configs = json.load(open('config.json'))
db_file_name=configs['servers_remaining']
servers_manual=configs['servers_manual']

logger = utils.get_logger(os.path.basename(__file__))

## Servers specified on command line parameters take precedence over those servers within the file.
## python xxx.py  ip1 ip2 ip3...
## python xxx.py
def main():
    server_list=sys.argv[1:]
    if len(server_list) == 0:
        with open(servers_manual) as f : server_list = f.readlines()
        logger.info('using servers in file.')
    server_list = list(map(lambda host: host.strip(), server_list))
    logger.info('servers: {}'.format(server_list))
    ## import the public IPs listed in the servers.manual.txt into servers.remaining.db to deploy
    with sqlite3.connect(db_file_name) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS server(host text)')
        for host in server_list:
            conn.execute('INSERT INTO server VALUES ( :host )', { "host": host })
        print("#################### Hosts have been imported to sqlite database to reploy! ####################")

    parallel_run(deploy)  ## deploy concurrently

if __name__ ==  '__main__':
    if os.path.exists(db_file_name): os.remove(db_file_name)
    main()