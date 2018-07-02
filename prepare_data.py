import sys, os, json, sqlite3
from functools import wraps
import utils;
configs = utils.get_config()
db_file_name=configs['servers_remaining']
servers_manual=configs['servers_manual']
servers_all_name = configs['servers_all']

logger = utils.get_logger(os.path.basename(__file__))

## Servers specified on command line parameters take precedence over those servers within the file.
## python xxx.py  ip1 ip2 ip3...
## python xxx.py
def prepare_custom_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip_address = configs['ipAddress']
        server_list = ip_address.split()
        if len(server_list) == 0:
            with open(servers_manual) as f: server_list = f.readlines()
            logger.info('using servers in file.')
        server_list = list(map(lambda host: host.strip(), server_list))
        logger.info('servers: {}'.format(server_list))
        if os.path.exists(db_file_name):
            os.remove(db_file_name)
            logger.info(db_file_name + " is removed before importing hosts.")
        ## import the public IPs listed in the servers.manual.txt into servers.remaining.db to deploy
        with sqlite3.connect(db_file_name) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS server(host TEXT)')
            for host in server_list:
                conn.execute('INSERT INTO server VALUES ( :host )', {"host": host})
            print("#################### Hosts have been imported to sqlite database to reploy! ####################")
        return func(*args, **kwargs)
    return wrapper


def prepare_all_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        servers = json.load(open(servers_all_name))
        has_db_file = os.path.exists(db_file_name)
        with sqlite3.connect(db_file_name) as conn:
            if not has_db_file:  ## first time deployment
                conn.execute('CREATE TABLE IF NOT EXISTS server(host text)')
                instanceIds = list(map(lambda item: {"host": item['publicHost']}, servers))
                conn.executemany('INSERT INTO server VALUES ( :host )', instanceIds)  ## instanceIds should be a list of tuples
        return func(*args, **kwargs)
    return wrapper


