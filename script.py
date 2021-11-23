# Nama: Harya Anggitama
# NIM : 123190125
# Untuk menjalankan program dibutuhkan import library pycrypto
# Bisa dengan memasukkan command "pip install pycrypto" pada terminal

from Crypto.Cipher import AES
from Crypto import Random
import os
import os.path
from os import listdir
from os.path import isfile, join
import time

class Enkriptor:
    def __init__(self, key):
        self.key = key

    # Pembuatan pad bertujuan agar key yang dimasukan berukuran 16bit
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    
    def enkripsi(self, message, key, key_size = 256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def enkripsi_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.enkripsi(plaintext, self.key)
        with open(file_name + ".enc", "wb") as fo:
            fo.write(enc)
        os.remove(file_name)
    
    def dekripsi(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b'\0')
    
    def dekripsi_file(self, file_name):
        with open(file_name, "rb") as fo:
            ciphertext = fo.read()
        dec = self.dekripsi(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def get_all_files(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def enkripsi_semua_file(self):
        dirs = self.get_all_files()
        for file_name in dirs:
            self.enkripsi_file(file_name)

    def dekripsi_semua_file(self):
        dirs = self.get_all_files()
        for file_name in dirs:
            self.dekripsi_file(file_name)
    
key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Enkriptor(key)
clear = lambda: os.system("cls")

if os.path.isfile("data.txt.enc"):
    while True:
        password = str(input("PASSWORD: "))
        enc.dekripsi_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.enkripsi_file("data.txt")
            break

    while True:
        clear()
        choice = int(input(
            "1. ENKRIPSI FILE \n2. DEKRIPSI FILE \n3. ENKRIPSI SEMUA FILE DI DIREKTORI \n4. DEKRIPSI SEMUA FILE DI DIREKTORI \n5. EXIT\n "
        ))
        clear()
        if choice == 1:
            enc.enkripsi_file(str(input("NAMA FILE [ENKRIPSI]: ")))
        elif choice == 2:
            enc.dekripsi_file(str(input("NAMA FILE [DEKRIPSI]: ")))
        elif choice == 3:
            enc.enkripsi_semua_file()
        elif choice == 4:
            enc.dekripsi_semua_file()
        elif choice == 5:
            exit()
        else:
            print("INPUT NOMOR SALAH")
else:
    while True:
        clear()
        password = str(input("SETTING PASSWORD UTAMA: "))
        password_ulang = str(input("KONFIRMASI PASSWORD: "))
        if password == password_ulang:
            break
        else:
            print("PASSWORD TIDAK SESUAI")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.enkripsi_file("data.txt")
    print("MOHON RESTART PROGRAM")
    time.sleep(15)






