from task_dispatcher import parallel_run
from prepare_data import prepare_custom_data
from action import deploy, monitor

@prepare_custom_data
def main():
    parallel_run(deploy)  ## run tasks concurrently
    # logging.disable(logging.CRITICAL)
    # parallel_run(monitor)  ## run tasks concurrently

if __name__ ==  '__main__':
    main()

