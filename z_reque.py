from multiprocessing import allow_connection_pickling
import paramiko



host = "os-1872"
user = "loaduser"
password = "TGzz2R38"
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, allow_agent=False, look_for_keys=False)

sftp = client.open_sftp()


sftp.close()
