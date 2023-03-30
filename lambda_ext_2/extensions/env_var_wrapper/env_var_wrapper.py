#!/usr/bin/env python3

import sys
import os
import subprocess

args = sys.argv

print('hellloooooooo!!!')
print(' '.join(args[1:]))

os.environ['LAMBDA_EXT_TEST'] = str(os.environ.keys())

# output = subprocess.check_output(args[1:])

# print(output)
os.system(' '.join(args[1:]))
