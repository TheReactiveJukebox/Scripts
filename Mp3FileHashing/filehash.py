#!/usr/bin/env python3

import os
import hashlib
import sys

path = sys.argv[1]


def rename():
    for filename in os.listdir(path):
        m = hashlib.sha256()
        m.update(str(filename).encode('utf-8'))
        os.rename(path + "/" + filename, path + "/" + m.hexdigest() + ".mp3")


def reorganize():
    for filename in os.listdir(path):
        first = filename[0]
        second = filename[1]
        if not os.path.exists(path + "/" + first + "/" + second):
            os.makedirs(path + "/" + first + "/" + second)
        os.rename(path + "/" + filename, path + "/" + first + "/" + second + "/" + filename[2:])


rename()
reorganize()
