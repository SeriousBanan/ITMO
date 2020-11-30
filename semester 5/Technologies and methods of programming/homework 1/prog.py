#!/usr/bin/python
import configparser
import os
import sys
import glob
import stat
from ast import literal_eval
from hashlib import sha512
from time import sleep


def deamon():
    closed_names = config["DEFAULT"]["words"].split(",")

    temp_info = {}

    for name in os.listdir():
        for closed_name in closed_names:
            if name in glob.glob(closed_name):
                temp_info[name] = [os.stat(name).st_mode, (os.stat(name).st_uid, os.stat(name).st_gid)]

                os.chmod(name, stat.S_IRWXU)

    temp_config = configparser.ConfigParser()
    temp_config["DEFAULT"] = temp_info
    temp_config["PID"] = {"pid": str(os.getpid())}

    with open("temp.ini", "w") as configfile:
        temp_config.write(configfile)

    os.chmod("temp.ini", stat.S_IREAD | stat.S_IWRITE)

    while True:
        for name in os.listdir():
            for closed_name in closed_names:
                if name in glob.glob(closed_name) and name not in temp_info.keys():
                    os.remove(name)

        sleep(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Недостаточно аргументов для запуска.\nВведите: python3 prog.py start/finish [password]")
        sys.exit(1)

    status, password = sys.argv[1:]

    if status not in ["start", "finish"]:
        print("Введены неверные аргументы.\nВведите: python3 prog.py start/finish [password]")
        sys.exit(1)

    hash = sha512(password.encode()).hexdigest()

    config = configparser.ConfigParser()
    config.read("template.tbl")

    if len(config["DEFAULT"]["words"]) < 1:
        print("Введены неверные аргументы.\nВведите: python3 prog.py start/finish [password]")
        sys.exit(1)

    if status == "start":
        config["DEFAULT"]["pass_hash"] = hash

        with open("template.tbl", "w") as configfile:
            config.write(configfile)
        os.chmod("template.tbl", stat.S_IREAD | stat.S_IWRITE)

        print("Программа запущенна")
        deamon()

    elif status == "finish":
        if hash != config["DEFAULT"]["pass_hash"]:
            print("Неверный пароль")
            sys.exit(1)

        temp_config = configparser.ConfigParser()
        temp_config.read('temp.ini')

        try:
            os.kill(int(temp_config["PID"]["pid"]), 9)
            print("Deamon остановлен")
        except BaseException:
            print("Deamon не запущен")

        for name in temp_config['DEFAULT']:
            array = literal_eval(temp_config['DEFAULT'][name])
            os.chmod(name, array[0])

        print("Все права возвращены.")
        os.remove("temp.ini")
