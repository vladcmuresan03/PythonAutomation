from Switch import Switch
from Router import Router
from Device import Device
import json


def load_device_data(filename):
    #loads data from our .json file (filename) and returns it as a dictionary
    with open(filename, 'r') as file:
        return json.load(file)


def main() -> None:  # Main function
    device_loader = LoadData()
    devices = device_loader.load_device_data('devices.json')

    while True:  #loop to keep showing the menu until the user exits
        print("""
        =======================================
        ======= Network Automation Tool =======
        ============== Main Menu ==============
        =======================================

        Please select an option.
        1. Choose a device and configure it.
        2. Exit.
        """)

        choice = input("Enter your choice: ")

        if choice == '1':
            device_found = False
            selected_device = input("Please enter the desired device IP address: ")

            for device in devices:
                if not device_found:
                    try:
                        # Check if the 'ip_address' key exists in the current device and compare
                        if 'ip_address' in device and device['ip_address'] == selected_device:
                            device_found = True

                            # Check if it's a router or switch by using the 'type' key
                            if device['type'].lower() == 'router':
                                RouterConfigurationMenu(device)
                            elif device['type'].lower() == 'switch':
                                SwitchConfigurationMenu(device)

                    except (TimeoutError, ConnectionError, KeyError) as e:
                        print(f"Connection failed: {e}. Please check the device configuration.")

            if not device_found:
                print("Device not found. Sending you back to the main menu...")

        elif choice == '2':
            print("Exiting application...")
            exit()  # Exit the while loop, terminating the program

        else:
            print("Invalid option. Please try again.")


def RouterConfigurationMenu(device) -> None:  # Configuration menu for routers.
    router_instance = Router(device['hostname'], device['ip_address'], device['username'], device['password'], device['exec_password'])

    while True:
        print("""
        The following configuration options are available for the Router:
        1. Configure HSRP for a Vlan.
        2. Configure a DHCP server.
        3. Set up RIPv2.
        4. Ping another device.
        5. Disconnect from the device and return to Main Menu.
        """)
        config_choice = input("Enter your choice: ")

        if config_choice == '1':
            router_instance.config_hsrp()
            break  # Exit the loop after valid selection
        elif config_choice == '2':
            router_instance.setup_dhcp(device['ip_address'])
            break
        elif config_choice == '3':
            router_instance.config_ripv2()
            break
        elif config_choice == '4':
            device_instance = Device(device['hostname'], device['ip_address'], device['username'], device['password'], device['exec_password'])
            device_instance.ping()
            break
        elif config_choice == '5':
            main()
            break
        else:
            print("Please enter a valid option.")

def SwitchConfigurationMenu(device) -> None:  # Configuration menu for switches.
    switch_instance = Switch(device['hostname'], device['ip_address'], device['username'], device['password'], device['exec_password'])

    while True:
        print("""
        The following configuration options are available for the Switch:
        1. Configure a Vlan.
        2. Configure Security.
        3. Configure STP.
        4. Ping another device.
        5. Disconnect from the device and return to Main Menu.
        """)
        config_choice = input("Enter your choice: ")

        if config_choice == '1':
            switch_instance.config_vlan()
            break  # Exit the loop after valid selection
        elif config_choice == '2':
            switch_instance.config_security()
            break
        elif config_choice == '3':
            switch_instance.config_stp()
            break
        elif config_choice == '4':
            device_instance = Device(device['hostname'], device['ip_address'], device['username'], device['password'], device['exec_password'])
            device_instance.ping()
            break
        elif config_choice == '5':
            main()
            break
        else:
            print("Please enter a valid choice.")

class LoadData:
    _instance = None
    _device_data = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoadData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def load_device_data(self, filename):
        if self._device_data is None:
            with open(filename, 'r') as file:
                self._device_data = json.load(file)
        return self._device_data