#!/usr/bin/env python3

import exif
import crc
import datetime

def _get_season(month):
    m = int(month)
    if m in [3,4,5]:
        return "spring"
    elif m in [6,7,8]:
        return "summer"
    elif m in [9,10,11]:
        return "fall"

    # [12,1,2]:
    return "winter"

def mangle(filename: str):
    newname = filename

    with open(filename, 'rb') as image_file:
        image = exif.Image(image_file)

    year = datetime.date.today().year
    month = datetime.date.today().month

    if image.has_exif:
        date,time = image.datetime.split(" ")
        year,month,day = date.split(":")
        hour,minute,second = time.split(":")

        checksum = crc.CrcCalculator(crc.Crc8.CCITT).calculate_checksum(bytes(str(filename), 'ascii'))

        newname = "{}-{}-{}_{}_{}_{}_{:02x}.jpg".format(year,month,day,hour,minute,second, checksum)

    return year, _get_season(month), newname
