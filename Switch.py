from Connection import Connection

class Switch:
    def __init__(self, name, ip_address, username, password, exec_pass):
        self.name = name
        self.connection = Connection(ip_address, username, password)
        self.exec_pass = exec_pass

    def config_portchannel(self):
        self.connection.connect(self.exec_pass)
        stdout, stderr = self.connection.send_command('comanda port-channel')
        self.connection.close()

    def config_security(self):
        self.connection.connect(self.exec_pass)
        stdout, stderr = self.connection.send_command('comenzi security')
        self.connection.close()

    def ping(self):
        self.connection.connect(self.exec_pass)
        stdout, stderr = self.connection.send_command('comanda static route')
        self.connection.close()