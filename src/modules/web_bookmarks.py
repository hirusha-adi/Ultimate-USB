from browser_history import get_bookmarks
import os


class WebBookmarks:
    def __init__(self, csv: bool = None, json: bool = None, error_file=None):
        self._csv = csv
        self._json = json
        self._error_file = error_file
        self._outputs = None

    def getOutput(self):
        try:
            self._outputs = get_bookmarks()
        except Exception as e:
            if self._error_file:
                self._error_file.write(f"{e}")

    def setCsv(self, csv: bool = True):
        self._csv = csv

    def setJson(self, json: bool = True):
        self._json = json

    def run(self,
            json_file_name: str,
            csv_file_name: str,
            csv: bool = None,
            json: bool = None
            ):

        if not(csv is None):
            self._csv = csv
        if not(json is None):
            self._json = json

        self.getOutput()

        if self._csv:
            self._outputs.save(csv_file_name)

        if self._json:
            self._outputs.save(json_file_name)
