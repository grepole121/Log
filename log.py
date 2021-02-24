import time, os, os.path, getpass
from pass_key_gen import gen_key
from cryptography.fernet import Fernet

if not os.path.isfile('key.key'):
    #Create a key with a user password if the key doesn't exist
    gen_key(getpass.getpass("Please enter your password: "))

f = Fernet(open("key.key", "rb").read())
file_destination = "/home/george/MEGA/Log/New/log.txt"


def encrypt():
    #Encrypt the file after changes have been made
    with open(file_destination, "rb") as log:
        log_data = log.read()
    encrypted_log = f.encrypt(log_data)
    with open(file_destination, "wb") as log:
        log.write(encrypted_log)


def decrypt():
    #Decrypt the file so changes can be written
    if os.path.isfile(file_destination):
        with open(file_destination, "rb") as log:
            encrypted_data = log.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(file_destination, "wb") as log:
            log.write(decrypted_data)


date = time.strftime('%d/%m/%Y')
time = time.strftime('%H:%M:%S')
print('What would you like to append')
log_input = input()
decrypt()
with open(file_destination, 'a') as myfile:
    myfile.write('[ ' + date + ' - ' + time + ' ] - ' + log_input + '\n')
encrypt()