from browser_history import get_history
import os


class WebHistory:
    def __init__(self, csv: bool, json: bool):
        self._csv = csv
        self._json = json

        self._outputs = get_history()

    def setCsv(self, csv: bool = True):
        self._csv = csv

    def setJson(self, json: bool = True):
        self._json = json

    def saveHistory(self,
                    json_file_name: str,
                    csv_file_name: str,
                    csv: bool = None,
                    json: bool = None
                    ):
        if not(csv is None):
            self._csv = csv
        if not(json is None):
            self._json = json

        if self._csv:
            self._outputs.save(csv_file_name)

        if self._json:
            self._outputs.save(json_file_name)

    def run(self, csv: bool, json: bool,
            json_file_name: str, csv_file_name: str):
        self.saveHistory(
            csv=csv,
            json=json,
            json_file_name=json_file_name,
            csv_file_name=csv_file_name)
