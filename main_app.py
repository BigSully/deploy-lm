from datetime import datetime
import os, time
import deploy_app, utils

logger = utils.get_logger(os.path.basename(__file__))

def deploy(node, context):
    ## execute command,  stop ->pass file ->startbg
    prefix = context['serverRoot']  #  /home/appadmin/jazmin_server
    instance = context['instance']  # instance/112a74a102a116
    localpath=context['localPackage']  ## /home/operationer/.jenkins/workspace/newkand/KandSubSystem/build/libs/KandSubSystem.jaz
    remotepath=prefix + "/" + instance + "/" + context['packageName'] ## /home/appadmin/jazmin_server/instance/112a74a102a116/KandSubSystem.jaz
    jazmin_pid_path = prefix + "/" + instance + "/" + "jazmin.pid" ## /home/appadmin/jazmin_server/instance/112a74a102a116/jazmin.pid
    cmdKillJaz = "pkill -f /home/appadmin/jazmin_server/jazmin.jar; sleep 1"
    dirname = os.path.dirname(remotepath)
    cmdMakeDir = "mkdir -p " + dirname
    cmdChangeDirectory = 'cd ' + prefix  ## change current directory
    cmdStopJazmin=context['stopCommand'] + " " + instance   # /home/appadmin/jazmin_server/jazmin stop  instance/112a74a103a124
    cmdClearPid="cat /dev/null > {}".format(jazmin_pid_path)
    cmdStartJazmin=context['startCommand']  + " " +  instance  # /home/appadmin/jazmin_server/jazmin startbg  instance/112a74a103a124
    cmdPath = "PATH='/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin'";   ## just to resolve "ifconfig cannot be found"

    cmdGroup01 = " && ".join( [cmdPath, cmdChangeDirectory, cmdKillJaz, cmdMakeDir] )  ## These commands should succeed at the same time.
    node.exec(cmdGroup01)
    node.upload(localpath, remotepath)
    cmdGroup02 = " && ".join( [cmdPath, cmdClearPid, cmdStartJazmin] )
    node.exec(cmdGroup02)

def monitor(node, context):
    result = node.exec("ps -ef | grep jaz")
    host = context['publicHost']
    logger.info("##host: {}, message: {}".format(host, result))
    # time.sleep(120)

def main():
    startTime=datetime.now()
    logger.info("##starting time: {}".format(startTime))
    deploy_app.parallel_deploy(deploy)  ## deploy concurrently
    endTime=datetime.now()
    seconds=(endTime - startTime).seconds
    minutes=seconds//60
    seconds=seconds%60
    logger.info("##end time: {}".format(endTime))
    logger.info("#################### tasks have finished in {} minutes {} seconds!! ####################".format(minutes, seconds))

if __name__ ==  '__main__':
    main()
    ## 多执行几遍也不会有副作用，适用于易于失败的部署!!
    # main()
    # main()