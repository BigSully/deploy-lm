from prepare_data import prepare_all_data
from task_dispatcher import parallel_run
from action import deploy, profiling

@prepare_all_data
@profiling
def main():
    parallel_run(deploy)  ## deploy concurrently

if __name__ ==  '__main__':
    main()
    ## 多执行几遍也不会有副作用，适用于易于失败的部署!!
    # main()
    # main()