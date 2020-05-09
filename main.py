from prepare_data import prepare_all_data, prepare_custom_data
from parallelizer import parallel_run
from task import deploy, profiling, monitor

# @prepare_custom_data  # keep executing tasks on the rest of the servers after interruption or exit
@prepare_all_data
@profiling
def main():
    parallel_run(deploy)  ## run tasks concurrently
    # logging.disable(logging.CRITICAL)
    # parallel_run(monitor)  ## run tasks concurrently

if __name__ ==  '__main__':
    main()
    ## 多执行几遍也不会有副作用，适用于易于失败的部署!!
    # main()
    # main()