import sys
import re

def protect_miss_comma_split(s):
    protect = False
    lock = ''
    for i, c in enumerate(s):
        if protect == False and (c == '\"' or c == '\''):
            protect = True
            lock = c
        if c == ',' and protect == True:
            s = s[:i] + '#$@%' + s[i + 1:]
        if c == ',' and protect == True and lock == c:
            protect = False
            lock = ''
    return s.replace('\"', '')


if '-h' in sys.argv:
    print('You see this message because you run program with [-h] help flag.')
    print('This script will convert DB dump file with values separated by any delimiter to XML format. <TABLE_NAME COLUMN=\"value\" ... />')
    print('Remember, if you convert from non-standard DB output then first file line should be column names separated by the same separator as values.\n')
    print('Available flags:')
    print('[-nodataset] flag will exclude <dataset></dataset> tag from output file.')
    print('[-noformat] flag will exclude <?xml?> tag from output file.')
    print('[-tabsize=N] flag will set desired tab size for nested tags. N must be an integer')
    print('[-trim=boolean] if true - script will cut whitespaces at the beginning and end of each DB cell. false by default expect of for standatrd SQL response format. Script detecs this format automatically.')
    exit(1)

print('Run with [-h] flag to see additional options')
adddatasettag = False if '-nodataset' in sys.argv else True
addxmlformat = False if '-noformat' in sys.argv else True
tabsize = 4
separator = ','
trim = False
for arg in sys.argv:
    if re.match(r'-tabsize=[0-9]+', arg): tabsize = int(arg[arg.find('=') + 1:])
    if re.match(r'-separator=.+', arg): separator = arg[arg.find('=') + 1:]
    if re.match(r'-trim=.+', arg):
        trm = arg[arg.find('=') + 1:]
        trim = True if trm.lower() == 'true' else False

print('SQL query execution result file path: ', end='')
filename = input()
print('Table name: ', end='')
table = input()

try:
    with open(filename, 'r+') as f: data = f.read()
except:
    print('[ERROR] Cannot find file specified')
    exit(-1)

sql = []
is_standard = False
for line in data.split('\n'):
    if re.match('[-+]+', line) and is_standard == False:
        is_standard = True
        separator = '|'
    if line != '' and not re.match('[-+]+', line):
        row = []
        line = protect_miss_comma_split(line)
        for splited in line.split(separator):
            if is_standard or trim == True: splited = splited.strip()
            splited = splited.replace('#$@%', ',')
            row.append(splited)
        if is_standard: row = row[1:-1]
        sql.append(row)

if sql[-1] == [] or sql[-1] == ['']: sql = sql[:-1]

xml = []
i = 1
if addxmlformat: xml.append('<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n')
if adddatasettag: xml.append('<dataset>\n')
while i < len(sql):
    k = 0
    str = ''.join([' ' for _ in range(tabsize)])
    str += '<' + table +' '
    while k < len(sql[i]):
        try: str += sql[0][k] + '=\"' + sql[i][k] + '\" '
        except:
            print('[ERROR] Parse error occurred while processing file. Cant parse file, make sure you have same number of columns in each row and your separator is set to right value.')
            print('Run program with [-h] flag too see available options and also to see separator setup option. Default separator is comma.')
            exit(-1)
        k+= 1
    str += '/>\n'
    xml.append(str)
    i += 1

if adddatasettag: xml.append('</dataset>\n')

newfile = table + '_dump.xml'
resfile = open(newfile, 'w+')
resfile.writelines(xml)
resfile.close()
