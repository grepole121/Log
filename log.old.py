#Ubuntu log code
import time
date = time.strftime('%d/%m/%Y')
time = time.strftime('%H:%M:%S')
print 'What would you like to append'
log_event = raw_input()
with open('/home/george/MEGA/Log/New/log.txt', 'a') as myfile:
    myfile.write('[ ' + date + ' - ' + time + ' ] - ' + log_event + '\n')
