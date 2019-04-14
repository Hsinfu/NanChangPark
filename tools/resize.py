import subprocess

for i in range(48):
    cmd = 'convert {:05d}.png -resize 1440 {:05d}.png'.format(i, i)
    subprocess.check_output(cmd, shell=True)

