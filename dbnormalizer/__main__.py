import os
import subprocess

__author__ = 'Maira'

file_path = os.path.abspath(os.path.dirname(__file__))+'/web/web.py'
try:
    subprocess.call(["python3", file_path])
except OSError as e:
    subprocess.call(["python", file_path])