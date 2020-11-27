import sys
import os
import pickle

PROG_LIMITS_FOLDER_PATH = "~/.TIMP 2 prog limits"

with open(os.path.join(os.path.expanduser(PROG_LIMITS_FOLDER_PATH), "startup times left"), "r") as file:
    startup_times_left = int(file.read())

if not startup_times_left:
    print("Бесплатный лимит запусков кончился, приобретите полную версию!")
    sys.exit()

print(f"Оставшееся количество бесплатных запусков программы: {startup_times_left - 1}")

with open(os.path.join(os.path.expanduser(PROG_LIMITS_FOLDER_PATH), "startup times left"), "w") as file:
    print(startup_times_left - 1, file=file)

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
