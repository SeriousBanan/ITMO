#!/usr/bin/python
import argparse
import configparser
import os
import glob
from ast import literal_eval
from hashlib import sha512
from time import sleep


def run():
    banned_words = config['DEFAULT']['words'].split(',')
    dir_list = os.listdir()
    temp = {}  # file for save priveleges

    for name in dir_list:
        for ban in banned_words:
            if name in glob.glob(ban):
                temp[name] = [os.stat(name).st_mode,
                              (os.stat(name).st_uid,
                               os.stat(name).st_gid)]
                # os.chown(name, 0, 0)
                os.chmod(name, 0o0700)  # read

    temp_config = configparser.ConfigParser()
    temp_config['DEFAULT'] = temp
    temp_config['PID'] = {'pid': str(os.getpid())}

    with open('temp.ini', 'w') as configfile:
        temp_config.write(configfile)
    os.chmod('temp.ini', 0o0600)

    while True:
        dir_list = os.listdir()
        for name in dir_list:
            for ban in banned_words:
                if name in glob.glob(ban) and name not in temp.keys():
                    os.remove(name)
        sleep(1)


if __name__ == '__main__':
    arg = input('[\x1b[1;34m*\x1b[0m] Print: Start or finish? ')
    password = input('[\x1b[1;34m*\x1b[0m] Enter the password: ').encode()
    hash = sha512(password).hexdigest()

    config = configparser.ConfigParser()
    config.read('template.tbl')

    try:
        if arg == 'start':
            if len(config['DEFAULT']['words']) < 1:
                raise KeyError

            config['DEFAULT']['pass_hash'] = hash

            with open('template.tbl', 'w') as configfile:
                config.write(configfile)
            os.chmod('template.tbl', 0o0600)  # for rw users

            print('[\x1b[1;32m+\x1b[0m] Program launch ')

            run()

        elif arg == 'finish':
            if hash != config['DEFAULT']['pass_hash']:
                raise ZeroDivisionError

            temp_config = configparser.ConfigParser()
            temp_config.read('temp.ini')

            try:
                os.kill(int(temp_config['PID']['pid']), 9)
                print('[\x1b[1;32m+\x1b[0m] Stopped daemon!')
            except BaseException:
                print('[\x1b[1;31m-\x1b[0m] Daemon already stopped!')
                print('[\x1b[1;32m+\x1b[0m] Trying to return default permissions!')

            for name in temp_config['DEFAULT']:
                array = literal_eval(temp_config['DEFAULT'][name])
                # os.chown(name, array[1][0], array[1][1])
                os.chmod(name, array[0])

            print('[\x1b[1;32m+\x1b[0m] Returned all permissions to default!')

            os.remove('temp.ini')
        else:
            print('Try again!')
    except KeyError:
        print(
            '[\x1b[1;31m-\x1b[0m] Configuration file is corrupted, regenerate it please!')
    except ZeroDivisionError:
        print('[\x1b[1;31m-\x1b[0m] Incorrect password!')
    except BaseException:
        print('[\x1b[1;31m-\x1b[0m] Some unexpected error!')
