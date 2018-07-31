import subprocess
import commands

s = ''
with open('commits.txt') as f:
	for line in f:
		s = subprocess.call("git" + " cherry-pick --allow-empty " + line[:-1], shell=True)
		if s != 0:
			print '\n[ERROR] The following commit cannot be cherry-picked. It may have comflicts or does not exist.'
			print line
			break

