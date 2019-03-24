#!/usr/bin/env python3

from PIL import Image
import piexif
from datetime import datetime
from datetime import timedelta
import argparse

DATETIME_FORMAT="%Y:%m:%d %H:%M:%S"

#parse args
parser = argparse.ArgumentParser(description='Process date and time in exif data.', add_help=False)
parser.add_argument('file', type=open)
parser.add_argument('-d', '--days', default=0, type=int, dest='days')
parser.add_argument('-h', '--hours', default=0, type=int, dest='hours')
parser.add_argument('-m', '--minutes', default=0, type=int, dest='minutes')

args = parser.parse_args()

print("{}: adding {} days, {} hours and {} minutes".format(args.file.name, args.days, args.hours, args.minutes))

delta = timedelta(days=args.days, hours=args.hours, minutes=args.minutes)

im = Image.open(args.file.name)
exif_dict = piexif.load(im.info["exif"])

dateTime = exif_dict["0th"][0x132]
dt = datetime.strptime(dateTime.decode("ascii", "ignore"), DATETIME_FORMAT)

dtnew = dt + delta
dateTimeNew = datetime.strftime(dtnew, DATETIME_FORMAT).encode("ascii")

#DateTime
exif_dict["0th"][0x132] = dateTimeNew
#DateTimeOriginal
exif_dict["Exif"][0x9003] = dateTimeNew
#DateTimeDigitized
exif_dict["Exif"][0x9004] = dateTimeNew

exif_bytes = piexif.dump(exif_dict)
piexif.insert(exif_bytes, args.file.name)

print("{}: {} -> {}".format(args.file.name, dt, dtnew))
