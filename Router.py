from Device import Device

class Router(Device):

    def config_ripv2(self): #method for configuring rip on a router
        print("check")
        self.connection.connect(self.exec_pass)

        network1 = input("IP address of the first network: ")
        network2 = input("Ip address of the second network: ")
        redistribute = input("Should the static routes be redistributed? (Enter 'yes' or 'no')")

        if redistribute.lower() == "yes":
            red = True
        elif redistribute.lower() == "no":
            red = False
        self.connection.close()

    def config_route(self):
        self.connection.connect(self.exec_pass)
        stdout, stderr = self.connection.send_command('comanda static route')
        self.connection.close()

    def ping(self):
        self.connection.connect(self.exec_pass)
        stdout, stderr = self.connection.send_command('comanda static route')
        self.connection.close()