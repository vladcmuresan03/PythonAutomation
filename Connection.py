import paramiko

class Connection:
    def __init__(self, ip_address, username, password):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.client = None
        self.shell = None

    def connect(self, exec_pass):
        #establishing ssh connection and entering privileged exec mode
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.ip_address, username=self.username, password=self.password)

            #open a shell for multiple commands
            shell = self.client.invoke_shell()
            #sending enable command, entering exec mode and conf t
            shell.send('enable\n')
            shell.send(f'{exec_pass}\n')
            shell.send('conf t\n')

            #wait a short while for the execution of commands
            shell.settimeout(2.0) #set timeout to wait for max 2 secs instead of waiting forever
            output = shell.recv(1000).decode('utf-8')
            print(output)

            if "(config)#" in output:
                print("Successfully Connected to " + self.ip_address)
        except paramiko.ssh_exception.AuthenticationException:
            print("Authentication failed")
        except Exception as e:
            print(f"Error occurred: {e}")


    def send_command(self, command):
        if self.client is None:
            raise Exception("SSHClient not connected")

        #checks whether there is an open shell session; if not, opens one
        if self.shell is None:
            print("The shell session is not active; Trying to reestablish it.")
            try:
                self.shell = self.client.invoke_shell()
                if self.shell:
                    print("Shell session activated successfully.")
            except Exception as e:
                raise Exception("Reestablishing the shell session failed.") from e

        #send command
        self.shell.send(command + '\n')

        #wait for command output
        self.shell.settimeout(0.7)  #wait for receiving an output
        output = ""
        while True:
            try:
                part = self.shell.recv(1024).decode('utf-8')
                output += part
                if len(part) == 0:  #exits loop after all data is received
                    break
            except paramiko.ssh_exception.SSHException as e:
                break  #exits loop if no more data is available

        return output

    def disconnect(self) -> None:
        if self.shell:
            self.shell.close()
            self.shell = None
            print("Shell session closed on " + self.ip_address)

        if self.client:
            self.client.close()
            self.client = None
            print("Disconnected from " + self.ip_address)


