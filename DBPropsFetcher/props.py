import os

write_to = open('build.properties', 'a')
for root, directories, filenames in os.walk('/'):
	for directory in directories:
		pass
		# print os.path.join(root, directory) 
	for filename in filenames:
		if '.properties' in filename:
			f = open(os.path.join(root,filename), 'r+')
			if 'database.id' in f.read():
				f.close()
				f = open(os.path.join(root,filename), 'r+')
				write_to.write('# _________________________' + filename + '_________________________\n\n')
				for line in f:
					write_to.write('# ' + line + '\n')
				write_to.write('\n\n\n\n')
			print os.path.join(root,filename)
write_to.close()