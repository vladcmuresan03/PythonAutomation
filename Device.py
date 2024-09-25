import paramiko.ssh_exception
from Connection import Connection

class Device:
    def __init__(self, hostname, ip_address, username, password, exec_pass):
        self.ip_address = ip_address
        self.hostname = hostname
        self.username = username
        self.password = password
        self.exec_pass = exec_pass
        self.connection = Connection(ip_address, username, password)

    def ping(self) -> None: #shared method (routers AND switches) for pinging another device
        print("check")
        self.connection.connect(self.exec_pass)
        destination_ip = input("Enter the destination IP address: ")

        if self.connection.shell is None:
            print("Establishing a new shell session...")
            self.connection.shel = self.connection.client.invoke_shell()

        self.connection.shell.send(f'do ping {destination_ip}\n')

        output = ""
        self.connection.shell.settimeout(3)

        while True:
            try:
                part = self.connection.shell.recv(1024).decode('utf-8')
                output += part
                if len(part) == 0:
                    break
            except paramiko.ssh_exception.SSHException:
                break

        if "Reply from" in output:  # Adjust this string as necessary based on actual output
            print("Ping successful!")
            return True
        else:
            print("Ping failed.")
            return False

        self.connection.disconnect() #disconnect from the device


