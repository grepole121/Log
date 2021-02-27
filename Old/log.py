import time, os, os.path, getpass
from crypt import decrypt, encrypt

file_destination = "/home/george/MEGA/Log/New/log.txt"


date = time.strftime('%d/%m/%Y')
time = time.strftime('%H:%M:%S')
print('What would you like to append')
log_input = input()
decrypt()
with open(file_destination, 'a') as myfile:
    myfile.write('[ ' + date + ' - ' + time + ' ] - ' + log_input + '\n')
encrypt()