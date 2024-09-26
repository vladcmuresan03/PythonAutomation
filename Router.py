from Device import Device

class Router(Device):

    def config_ripv2(self): #method for configuring rip on a router
        self.connection.connect(self.exec_pass)

        network1 = input("IP address of the first network: ")
        network2 = input("IP address of the second network: ")

        while True:
            redistribute = input("Do you want to redistribute? (yes/no): ").lower()

            if redistribute == "yes":
                red = True
                break  # Exit the loop once a valid choice is made
            elif redistribute == "no":
                red = False
                break
            else:
                print("Please enter a valid choice. (yes/no)")

        commands = [
            'router rip',
            'version 2',
            'no auto-summary',
            f'network {network1}',
            f'network {network2}',
            'exit'
        ]

        for command in commands:
            stdout, stderr = self.connection.send_command(command)

        if red is True:
            stdout, stderr = self.connection.send_command('redistribute static\n')

        self.connection.close()

    def setup_dhcp(self, ip):
        #method for configuring dhcp on a router;
        #ip parameter = ip address to us as default gateway for the dhcp pool

        self.connection.connect(self.exec_pass)
        ip_prefix = '.'.join(ip.split('.')[:3])
        lan_identifier = input("ID of the LAN: ")
        dhcp_pool_ip = input("IP address of the DHCP pool: ")
        netmask = input("Subnet mask: ")
        switch_count = int(input("Number of switches in the LAN: "))
        router_count = int(input("Number of routers in the LAN: "))

        first_r_ip = router_count + 1 #calculate first available router ip
        last_sw_ip = 255 - switch_count #calculate last available switch ip

        commands = [
            f"ip dhcp pool LAN{lan_identifier}",
            f"network {dhcp_pool_ip} {netmask}",
            f"default-router {ip}",
            "dns-server 8.8.8.8",
            "exit",
            f"ip dhcp excluded-address {ip_prefix}.1 {ip_prefix}.{first_r_ip}",
            f"ip dhcp excluded-address {ip_prefix}.{last_sw_ip} {ip_prefix}.254"
        ]

        for command in commands:
            stdout, stderr = self.connection.send_command(command)

        self.connection.close()

    def config_hsrp(self) -> None:
        self.connection.connect(self.exec_pass)
        interface = input("Interface: ")
        id_standby = input("Standby interface ID: ")
        v_router = input("Virtual router IP address: ")
        prio = input("Priority: (default = 100 if there's no input)")
        if not prio.strip() or prio not in range(0, 256):
            prio = "100"

        commands = [
            f'interface {interface}',
            'standby version 2',
            f'standby {id_standby} ip {v_router}',
            f'standby {id_standby} priority {prio}',
            f'standby {id_standby} preempt'
        ]

        for command in commands:
            stdout, stderr = self.connection.send_command(command)

        self.connection.close()
