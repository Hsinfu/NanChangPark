import subprocess
from collections import namedtuple

TextSytle = namedtuple('TextSytle', ['fontsize', 'x', 'y'])
ImgStyle = namedtuple('ImgStyle', ['width', 'height', 'x', 'y'])
LocationStyle = namedtuple('LocationStyle', ['x', 'y'])


# Ex. instruction -> 'ls -al'
def command_line(instruction):
    subprocess.check_output(instruction, shell=True)
