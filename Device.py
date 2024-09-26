from Connection import Connection

class Device:
    def __init__(self, hostname, ip_address, username, password, exec_pass):
        self.ip_address = ip_address
        self.hostname = hostname
        self.username = username
        self.password = password
        self.exec_pass = exec_pass
        self.connection = Connection(ip_address, username, password)

    def ping(self) -> None:  # shared method (routers AND switches) for pinging another device
        print("check ping meth")
        self.connection.connect(self.exec_pass)
        destination_ip = input("Enter the destination IP address: ")

        stdout, stderr = self.connection.send_command(f'do ping {destination_ip}')
        self.connection.shell.settimeout(5)


        if "3/5" in stdout or "4/5" in stdout or "5/5" in stdout:
            print("Ping successful!")
        else:
            print("Ping failed.")

        self.connection.close()  # close shell session

