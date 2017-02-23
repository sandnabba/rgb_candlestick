#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import time
from time import sleep
import rgb_patterns as p
import sys
import random

# functions = {
#     'a': p.studs(),
#     'b': p.random_studs(),
#     'c': p.vert_rb()
# }
#
# try:
#     program = int(sys.argv[1])
# except:
#     program = "a"
#     pass

#function = functions[program]

counter = 0

while 1:
    p.wave()
    p.studs()
    p.rb()
    p.fall()
