import os


def create_file_if_not_exist(path: str):
    if os.path.isfile(path):
        return True
    else:
        try:
            with open(path, "w", encoding="utf-8") as f_make:
                f_make.write("")
            return True
        except:
            return False


def create_folder_if_not_exists(path: str):
    if os.path.isdir(path):
        return True
    else:
        try:
            os.makedirs(path)
            return True
        except:
            return False


def add_seperator(topic: str, symbol="*", file=None):
    temp = "\n{seperator}\n{text}\n{seperator}".format(
        text=topic, seperator=str(symbol)*30)
    if file is None:
        return temp
    else:
        file.write(temp)
