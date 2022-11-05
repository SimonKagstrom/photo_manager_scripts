#!/bin/sh

MYDIR=$(dirname $(realpath $0))

mkdir -p ~/Pictures/incoming/
echo "Copying all files to the incoming directory"
gphoto2 --get-all-files --force-overwrite --hook-script="$MYDIR/hook_script.py"
if [ $? -eq 0 ]; then
    echo "Removing all files on the camera"
    gphoto2 --recurse --delete-all-files
fi
