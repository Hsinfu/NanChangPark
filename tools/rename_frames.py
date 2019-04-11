import subprocess

for i in range(48):
    cmd = 'mv bg_{:05d}.png {:05d}.png'.format(i, i)
    subprocess.check_output(cmd, shell=True)

