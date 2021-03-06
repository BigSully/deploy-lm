from concurrent.futures import ProcessPoolExecutor
import traceback, os, json, sqlite3
from node import Node
import utils

configs = utils.get_config()
db_file_name=configs['servers_remaining']  ## this variable should and will be shared among multiple processes, not just the main process!!
logger = utils.get_logger(os.path.basename(__file__))

def after_success(server):  ## 选择sqlite而不是文件的原因是文件会产生race condition，试了很多种办法都没能好好解决,而用sqlite3就不会有这个问题!!
    with sqlite3.connect(db_file_name) as conn:
        conn.execute("delete from server where host = :host", { "host": server['publicHost'] })

def task(context, index, action=None):
    with Node(context) as node:
        try:
            logger.info("##seq: {:03d}, host: {}".format(index+1, context['publicHost']))  ## print progress
            if action is not None: action(node, context)
            after_success(context)
        except:
            errMsg=traceback.format_exc()
            logger.error('【error】Deploying Failed, host: {}, error: {}'.format(node.host, errMsg))

def parallel_run(action=None):
    max_workers=configs['max_workers']
    servers_all_name=configs['servers_all']
    servers = determine_servers(servers_all_name, db_file_name)
    server_count=len(servers)
    if servers is None or server_count == 0: return
    if server_count < 20: max_workers=min(5, max_workers)  ## 剩余任务较少时减少进程数
    logger.info("##servers: {}, max workers: {}".format(server_count, max_workers))
    with ProcessPoolExecutor(max_workers) as executor:
        for index,server in enumerate(servers):
            executor.submit(task, server, index, action)
    logger.info("#################### {} tasks have finished!! ####################".format(server_count))


def determine_servers(servers_all_name, db_file_name):
    servers = json.load(open(servers_all_name))
    with sqlite3.connect(db_file_name) as conn:
        conn.row_factory = sqlite3.Row
        rows=conn.execute("select host from server")
        instanceIds = list(map(lambda row: row["host"], rows))
        candidate_servers = list(filter(lambda item: item['publicHost'] in instanceIds, servers))
        size=len(candidate_servers)
        if size > 0: logger.info("#################### {} servers remaining to continue! ####################".format(size))
        ## 重新部署如果剩下的服务器不足10台就打印出他们的id，以免某台一直无法部署成功
        if size > 0 and size < 10: logger.warning("#################### Servers to continue are less than 10, list: {} ####################".format(instanceIds))
        if size == 0: logger.warning("#################### No server is available, please remove file {} to continue! ####################".format(db_file_name))

    return candidate_servers
