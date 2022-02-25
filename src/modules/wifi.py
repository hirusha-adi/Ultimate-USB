import os
import subprocess
import src.utils.errors as error


class Wifi:
    def __init__(self, file=None, error_file=None):
        self.output = ""
        self.file = file
        self.error_file = error_file

    def runCommand(self):
        try:
            return subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(
                'utf-8', errors="backslashreplace").split('\n')
        except Exception as e:
            if self.error_file:
                self.error_file.write("\n{err}".format(err=e))
            raise error.WifiPasswordError

    def processOutput(self):
        data = self.runCommand()
        profiles = [i.split(":")[1][1:-1]
                    for i in data if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(
                    'utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1]
                           for b in results if "Key Content" in b]
                try:
                    self.output += "\n{:<30}|  {:<}".format(i, results[0])
                except IndexError:
                    self.output += "\n{:<30}|  {:<}".format(i, "")
            except subprocess.CalledProcessError:
                self.output += "\n{:<30}|  {:<}".format(i, "ENCODING ERROR")
            except Exception as e:
                if self.error_file:
                    self.error_file.write("\n{err}".format(err=e))

    def getOutput(self):
        if self.output:
            return self.output
        else:
            return "'Wifi.run()' has not been called yet"

    def getOutputFile(self):
        if self.output:
            try:
                self.file.write(self.output)
            except Exception as e:
                if self.error_file:
                    self.error_file.write("\n{err}".format(err=e))
        else:
            if self.error_file:
                self.error_file.write("'Wifi.run()' has not been called yet")

    def run(self):
        self.processOutput()
        if self.file:
            self.getOutputFile()


if __name__ == "__main__":
    import time
    if os.name == 'nt':
        with open("wifi-output.txt", "w+", encoding="utf-8") as file_wifi_passwords, open("errors.txt", "w+", encoding="utf-8") as file_wifi_passwords_errors:
            file_wifi_passwords.write(
                "{seperator}\nWifi Passwords\n{seperator}".format(seperator='*'*20))
            file_wifi_passwords_errors.write(
                "{seperator}\nWifi Passwords\n{seperator}".format(seperator='*'*20))
            obj = Wifi(file=file_wifi_passwords,
                       error_file=file_wifi_passwords_errors)
            obj.run()
            print(obj.getOutput())
        time.sleep(10)
