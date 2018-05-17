from datetime import datetime
import os, time
import utils
import functools

logger = utils.get_logger(os.path.basename(__file__))

def profiling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('LOG: Running job "%s"' % func.__name__)
        start_time = datetime.now()
        logger.info("##starting time: {}".format(start_time))
        result = func(*args, **kwargs)
        end_time = datetime.now()
        seconds = (end_time - start_time).seconds
        minutes = seconds // 60
        seconds = seconds % 60
        logger.info("##end time: {}".format(end_time))
        logger.info("#################### tasks have finished in {} minutes {} seconds!! ####################".format(minutes,seconds))
        logger.info('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper

@profiling
def deploy(node, context):
    ## execute command,  stop ->pass file ->startbg
    prefix = context['serverRoot']  #  /home/appadmin/jazmin_server
    instance = context['instance']  # instance/112a74a102a116
    local_path=context['localPackage']  ## /home/operationer/.jenkins/workspace/newkand/KandSubSystem/build/libs/KandSubSystem.jaz
    remote_path=prefix + "/" + instance + "/" + context['packageName'] ## /home/appadmin/jazmin_server/instance/112a74a102a116/KandSubSystem.jaz
    jazmin_pid_path = prefix + "/" + instance + "/" + "jazmin.pid" ## /home/appadmin/jazmin_server/instance/112a74a102a116/jazmin.pid
    cmd_kill_jaz = "pkill -f /home/appadmin/jazmin_server/jazmin.jar; sleep 1"
    dirname = os.path.dirname(remote_path)
    cmd_make_dir = "mkdir -p " + dirname
    cmd_change_dir = 'cd ' + prefix  ## change current directory
    cmd_stop_jazmin=context['stopCommand'] + " " + instance   # /home/appadmin/jazmin_server/jazmin stop  instance/112a74a103a124
    cmd_clear_pid="cat /dev/null > {}".format(jazmin_pid_path)
    cmd_start_jazmin=context['startCommand']  + " " +  instance  # /home/appadmin/jazmin_server/jazmin startbg  instance/112a74a103a124
    cmd_path = "PATH='/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin'";   ## just to resolve "ifconfig cannot be found"

    cmd_group01 = " && ".join( [cmd_path, cmd_change_dir, cmd_kill_jaz, cmd_make_dir] )  ## These commands should succeed at the same time.
    node.exec(cmd_group01)
    node.upload(local_path, remote_path)
    cmd_group02 = " && ".join( [cmd_path, cmd_clear_pid, cmd_start_jazmin] )
    node.exec(cmd_group02)

@profiling
def monitor(node, context):
    result = node.exec("ps -ef | grep jaz")
    host = context['publicHost']
    logger.info("##host: {}, message: {}".format(host, result))
    # time.sleep(120)
