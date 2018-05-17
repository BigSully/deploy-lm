import os, json
from task_dispatcher import parallel_run
from prepare_custom_data import prepare_data
from action import deploy, monitor

@prepare_data
def main():
    parallel_run(monitor)  ## run tasks concurrently

if __name__ ==  '__main__':
    configs = json.load(open('config.json'))
    db_file_name = configs['servers_remaining']
    if os.path.exists(db_file_name): os.remove(db_file_name)
    main()
    ## 多执行几遍也不会有副作用，适用于易于失败的部署!!
    # main()
    # main()
