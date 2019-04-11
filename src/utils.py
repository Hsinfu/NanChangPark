import subprocess
from collections import namedtuple

Color = namedtuple('Color', ['r', 'g', 'b'])
TextSytle = namedtuple('TextSytle', ['fontsize', 'x', 'y'])
ImgStyle = namedtuple('ImgStyle', ['width', 'height', 'x', 'y'])


# Ex. instruction -> 'ls -al'
def command_line(instruction):
    subprocess.check_output(instruction, shell=True)
