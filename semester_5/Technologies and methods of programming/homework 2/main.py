import time
import sys
import os
from os.path import expanduser

TIME_LIMITED = 1  # 1 - ограничено по времени, 2 - по использованиям
TIME_LIMIT = 300  # секунд
USES_LIMIT = 4  # раз

reached = 0
if TIME_LIMITED:
    flimit = open(os.path.join(expanduser("~"), '.pay_to_use/install_time'))
    install_time = float(flimit.read())
    now_time = time.time()
    if (now_time - install_time) > TIME_LIMIT:
        print("Ваше время использования бесплатной версии программы закончилось. Приобретите полную версию.")
        sys.exit()
    print("Ваше оставшееся время использования бесплатной версии: " +
          str(TIME_LIMIT - now_time + install_time))
    flimit.close()
else:
    flimit = open(os.path.join(expanduser("~"), '.pay_to_use/times_used'))
    times_used = float(flimit.read())
    if times_used >= USES_LIMIT:
        print("Ваши использования бесплатной версии программы закончились. Приобретите полную версию.")
        sys.exit()
    print("Ваше оставшееся количество использований бесплатной версии: ",
          str(USES_LIMIT - times_used - 1))
    flimit.close()
    flimit = open(os.path.join(expanduser("~"), '.pay_to_use/times_used'), 'w')
    flimit.write(str(times_used + 1))
    flimit.close()

f = open('hist', 'r+')
hist = [line for line in f]
name = raw_input("Введите ваше ФИО: ")
try:
    hist.index(name + '\n')
except ValueError:
    f.write(name + '\n')
else:
    print("Такое ФИО уже существует.")
