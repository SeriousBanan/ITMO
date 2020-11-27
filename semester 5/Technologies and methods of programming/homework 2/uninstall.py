import os

PROG_FOLDER_PATH = "~/TIMP 2 prog"

for dirpath, dirnames, filenames in os.walk(os.path.expanduser(PROG_FOLDER_PATH)):
    for filename in filenames:
        os.remove(os.path.join(dirpath, filename))
    for dirname in dirnames:
        os.removedirs(os.path.join(dirpath, dirname))
    break

os.rmdir(os.path.expanduser(PROG_FOLDER_PATH))
