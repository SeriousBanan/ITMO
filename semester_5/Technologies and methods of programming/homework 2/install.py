import tarfile
import os
from os.path import expanduser
import time

tar = tarfile.open("pack.tar")
os.chdir(expanduser("~"))
tar.extractall("./my_program")
tar.close()

if not os.path.isdir('.pay_to_use'):
    os.mkdir('.pay_to_use')
    install_time = open('.pay_to_use/install_time', 'w')
    install_time.write(str(time.time()))
    install_time.close()
    times_used = open('.pay_to_use/times_used', 'w')
    times_used.write('0')
    times_used.close()
else:
    print("Обнаружена предыдущая инсталляция.")
