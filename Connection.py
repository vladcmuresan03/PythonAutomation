import paramiko
from time import sleep

class Connection:
    def __init__(self, ip_address, username, password):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.client = None
        self.shell = None

    def connect(self, exec_pass) -> None:
        try:
            #establishing ssh connection and entering privileged exec mode
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip_address, username=self.username, password=self.password)

            #open a shell for multiple commands
            self.shell = self.client.invoke_shell()

            #sending enable command, entering exec mode and conf t
            self.shell.send('conf t\n')

            sleep(2) #set timeout to wait for max 2 secs instead of waiting forever

        except paramiko.SSHException as e:
            print(f"Error occurred: {e}")
            self.close()


    def send_command(self, command): #method used for sending a command to the selected device
        if not self.shell:
            print("Connection not established. Please connect first.")
            return None, "Connection not established."

        self.shell.send(command + '\n')
        sleep(3)

        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(1024).decode('utf-8')

        return output, ""

    def close(self) -> None:
        if self.client:
            #self.shell.send('\ndo wr\n')
            self.client.close()
            self.client = None
            self.shell = None

