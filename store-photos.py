#!/usr/bin/env python3

from importlib.resources import path
import shutil
import os
import pathlib
import sys

import image_mangler

def move_file(home, year, season, filename, newname):

    dstdir = os.path.join(home, "Pictures/outgoing/{}/{}".format(year, season))

    try:
        os.makedirs(dstdir)
    except:
        pass

    print("  {} -> {}".format(filename, os.path.join(dstdir, newname)))
    shutil.move(filename, os.path.join(dstdir, newname))

# https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree
def walk(path):
    for p in pathlib.Path(path).iterdir():
        if p.is_dir():
            yield from walk(p)
            continue
        yield p.resolve()

def mangle_directory(incoming : str, outgoing : str):
    try:
        os.makedirs(outgoing)
    except:
        pass

    print("moving files from {} to {}".format(incoming, outgoing))
    for filename in walk(incoming):
        if str(filename).lower().endswith(".jpg"):
            year, season, newname = image_mangler.mangle(filename)
            move_file(home, year, season, filename, newname)

def sync_to_rpi(outgoing : str):
    print("rsync to rpi4")
    return os.system("rsync -a {}/ pi@192.168.1.227:/mnt/photos/".format(outgoing))

def usage():
    print(
        "Usage: xxx [-n] [-r] [incoming] outgoing]\n"
        "\n"
        "  Where:"
        "    -n         Don't sync to RPi\n"
        "    -r         Don't remove incoming directory\n"
        "    incoming   The incoming directory (default ~/Pictures/incoming)\n"
        "    outgoing   The outgoing directory (default ~/Pictures/outgoing)\n"
    )
    sys.exit(1)

if __name__ == "__main__":

    home = os.path.expanduser("~")
    incoming = os.path.join(home, "Pictures/incoming")
    outgoing = os.path.join(home, "Pictures/outgoing")

    do_remove = "-n" not in sys.argv
    do_sync = "-r" not in sys.argv

    if "-h" in sys.argv:
        usage()

    path_args = [arg for arg in sys.argv[1:] if arg not in ["-r", "-n"]]

    if len(path_args) > 0:
        incoming = path_args[0]
    if len(path_args) > 1:
        outgoing = path_args[1]

    if not os.path.exists(incoming):
        print("The directory {} doesn't exist".format(incoming))
        sys.exit(1)

    if not os.path.exists(outgoing):
        os.makedirs(outgoing)


    mangle_directory(incoming, outgoing)

    if do_sync:
        if sync_to_rpi(outgoing) != 0:
            print("Could not sync to RPi")
            sys.exit(1)

        if do_remove:
            print("Removing {}".format(outgoing))
            shutil.rmtree(outgoing)
