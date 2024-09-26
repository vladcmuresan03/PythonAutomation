from Device import Device

class Switch(Device):

    def config_security(self): #method which configures security on a switch
        self.connection.connect(self.exec_pass)

        interface = input("Name of the interface you want security applied on: ")
        vlan = input("Name of VLAN to be allowed to pass through: ")

        commands = [
            f'int {interface}',
            'switchport port-security',
            'switchport mode access',
            f'switchport access vlan {vlan}',
            'spanning-tree bpduguard enable'
        ]

        for command in commands:
            stdout, stderr = self.connection.send_command(command)

        self.connection.close()

    def config_vlan(self):
        self.connection.connect(self.exec_pass)

        vlan_id = input("Please enter the ID of the VLAN you want to be created: ")
        vlan_name = input("Please enter the name of the VLAN you want to create: ")

        commands = [
            f'vlan {vlan_id}',
            f'name {vlan_name}'
        ]

        for command in commands:
            stdout, stderr = self.connection.send_command(command)

        self.connection.close()

    def config_stp(self):
        self.connection.connect(self.exec_pass)

        primary_vlan = input("ID of primary VLAN: (or type 'no' if you don't want to set it): ")
        secondary_vlan = input("ID of secondary VLAN: (or type 'no' if you don't want to set it): ")

        if primary_vlan != 'no' and secondary_vlan != 'no':
            stdout, stderr = self.connection.send_command(
                f'spanning-tree mode rapid-pvst\nspanning-tree vlan {primary_vlan} root primary\nspanning-tree vlan {secondary_vlan} root secondary\n')
        elif primary_vlan != 'no' and primary_vlan.isalnum() and secondary_vlan == 'no':
            stdout, stderr = self.connection.send_command(
                f'spanning-tree mode rapid-pvst\nspanning-tree vlan {primary_vlan} root primary\n')
        elif primary_vlan == 'no' and secondary_vlan != 'no' and secondary_vlan.isalnum():
            stdout, stderr = self.connection.send_command(
                f'spanning-tree mode rapid-pvst\nspanning-tree vlan {secondary_vlan} root secondary\n')
        elif primary_vlan == 'no' and secondary_vlan == 'no':
            print("Neither a primary or a secondary VLAN was chosen.")

        self.connection.close()