import subprocess


class RunCommand:
    def __init__(self, error_file=None, save_file=None):
        self.error_file = error_file
        self.save_file = save_file

    def setCommand(self, command):
        if (isinstance(command, list)) or (isinstance(command, tuple)):
            self._command = list(command)
        elif isinstance(command, str):
            temp = []
            for word in command.split(" "):
                temp.append(word)
            self._command = temp
        else:
            self._command = command

    def runCommand(self):
        data = subprocess.check_output(self._command).decode(
            'utf-8', errors="backslashreplace")
        return data

    def run(self, command=None):
        if not(command is None):
            self.setCommand(command=command)
        output = self.runCommand()

        if self.save_file:
            self.save_file.write(f"\n{output}")
        else:
            print(output)


if __name__ == "__main__":
    RunCommand().run(command="neofetch")
