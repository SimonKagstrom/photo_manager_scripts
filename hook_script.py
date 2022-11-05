#!/usr/bin/env python3

import os
import sys
import shutil

import image_mangler

def move_file(filename, newname):

    dstdir = os.path.join(os.path.expanduser("~"), "Pictures/incoming/")

    try:
        os.makedirs(dstdir)
    except:
        pass

    shutil.move(filename, os.path.join(dstdir, newname))

if __name__ == "__main__":

    if "ACTION" not in os.environ:
        print("ACTION and ARGUMENT needed in the environment")
        sys.exit(1)

    if os.environ["ACTION"] != "download":
        sys.exit(0)

    if "ARGUMENT" not in os.environ:
        print("ACTION=download, but no ARGUMENT")
        sys.exit(1)

    filename = os.environ["ARGUMENT"]

    year, season, newname = image_mangler.mangle(filename)

    print(year, season, newname)
    move_file(filename, newname)

    sys.exit(0)

