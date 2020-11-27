import time
import pickle
import sys
import os

TIME_LIMIT = 300
PROG_LIMITS_FOLDER_PATH = "~/.TIMP 2 prog limits"

with open(os.path.join(os.path.expanduser(PROG_LIMITS_FOLDER_PATH), "install time"), "r") as file:
    install_time = float(file.read())

if time.time() - install_time > TIME_LIMIT:
    print("Время бесплатного режима кончилось, приобретите полную версию!")
    sys.exit()

print(f"Оставшееся время бесплатного использования: {int(TIME_LIMIT - (time.time() - install_time))} сек.")

with open("users.dat", "rb") as file:
    users = pickle.load(file)

name = input("Введите ваше ФИО: ")

if name in users:
    print("Пользователь найден")
else:
    print("Пользователь добавлен")
    users.add(name)

with open("users.dat", "wb") as file:
    pickle.dump(users, file)
