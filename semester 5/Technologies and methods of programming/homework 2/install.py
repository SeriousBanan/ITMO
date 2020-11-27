import tarfile
import os
import time
import pickle

PROG_FOLDER_PATH = "~/TIMP 2 prog"
PROG_LIMITS_FOLDER_PATH = "~/.TIMP 2 prog limits"


with tarfile.open("data.tar.xz") as tar:
    tar.extractall(os.path.expanduser(PROG_FOLDER_PATH))

    with open(os.path.join(os.path.expanduser(PROG_FOLDER_PATH), "users.dat"), "wb") as file:
        pickle.dump(set(), file)


if not os.path.isdir(os.path.expanduser(PROG_LIMITS_FOLDER_PATH)):
    os.makedirs(os.path.expanduser(PROG_LIMITS_FOLDER_PATH))

    with open(os.path.join(os.path.expanduser(PROG_LIMITS_FOLDER_PATH), "install time"), "w") as file:
        print(time.time(), file=file)

    with open(os.path.join(os.path.expanduser(PROG_LIMITS_FOLDER_PATH), "startup times left"), "w") as file:
        print(5, file=file)

else:
    print("Программа уже была установлена.")
