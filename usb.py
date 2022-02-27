import os
import time

from src.modules.wifi import Wifi as Wifi_Passwords
import src.utils.file_manager as file_manager


class Main:
    def __init__(self):
        self.cwd = os.getcwd()

        self.output = os.path.join(self.cwd, "output")
        file_manager.create_folder_if_not_exists(self.output)

        self.error_file_name = os.path.join(self.output, "error.txt")
        file_manager.create_file_if_not_exist(self.error_file_name)
        self.error_file = open(self.error_file_name, "a+", encoding="utf-8")

    def run_Wifi_Passwords(self):
        file_manager.add_seperator(topic="Wifi Passwords",
                                   symbol="*",
                                   file=self.error_file)
        wifi_passwords_file_name = os.path.join(
            self.output, "wifi_passwords.txt")
        file_manager.create_file_if_not_exist(wifi_passwords_file_name)

        with open(wifi_passwords_file_name, "a+", encoding="utf-8") as wifi_passwords_file:
            file_manager.add_seperator(topic="Wifi Passwords",
                                       symbol="*",
                                       file=wifi_passwords_file)
            wifi_passwords_obj = Wifi_Passwords(file=wifi_passwords_file,
                                                error_file=self.error_file)
            wifi_passwords_obj.run()


Main().run_Wifi_Passwords()
