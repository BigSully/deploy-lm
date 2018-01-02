import traceback,os
import paramiko
import utils

logger = utils.getLogger(os.path.basename(__file__))

class Node:
    def __init__(self, context):
        self.host=context['privateHost']
        self.username=context['sshUser']
        self.password=context['sshPassword']

    def upload(self, localpath, remotepath):
        client = self.client
        sftp = client.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()

    def exec(self, cmd):
        client=self.client
        stdin,stdout,stderr = client.exec_command(cmd) ## uptime...
        errMsg=stderr.read()
        if len(errMsg) > 0:
            raise Exception("【error】cmd: {}, error: {}".format(cmd, errMsg))
        return stdout.read().decode("utf-8")  ## read bytes, decode it to string

    def init(self):
        self.client = paramiko.SSHClient()
        client = self.client
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.host, username=self.username, password=self.password)
        except paramiko.SSHException:
            errMsg=traceback.format_exc()
            logger.error('【error】Connection Failed, host: {}, error: {}'.format(self.host, errMsg))
            quit()

    def close(self):
        self.client.close()

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_value, traceback): self.close()


# # Testing
# import json
# servers = json.load(open('D:/RUBBISH/secureCRT_downloads/server_test.json'))  ## path!!!
# for server in servers:
#     with Node(server) as node:
#         node.exec("uptime")
