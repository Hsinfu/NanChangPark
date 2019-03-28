import subprocess

def random_positive_negative():
    return 1 if random(1) > 0.5 else -1

# Ex. instruction -> 'cp ../img/user.png ../img/user/'
def command_line(instruction):
    subprocess.check_output(instruction, shell=True)
