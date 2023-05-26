# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_opt.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: areheman <areheman@student.42mulhouse.fr>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/24 13:19:57 by areheman          #+#    #+#              #
#    Updated: 2023/05/26 11:15:35 by areheman         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib
import hmac
import struct
import argparse
import os
from my_eception import my_eception
from cryptography.fernet import Fernet
import random
import time
import sys
import qrcode
import tkinter as tk
from tkinter import font



QR_CODE_FILE="qr_code.png"

def check_hex_string(content):
	hex_dem="0123456789abcdefABCDEF"
	if len(content) < 64:
		raise my_eception(" Error: the key must be at list 64 hexadecimal characters.")
	for i in range(len(content)):
		if hex_dem.find(content[i]) == -1:
			raise my_eception(" Error: the {} character of the key is no hexadecimal characters.".format(i + 1))

def check_content(hex_path):
	content=""
	if hex_path.find('.') != -1:
		if not os.path.exists(hex_path):
			raise my_eception("Error :the {} file not be fond!".format(hex_path))
		f = open(hex_path,'r')
		for line in f:
			content = content + line
		f.close()
	else:
		check_hex_string(hex_path)
		content = hex_path
	check_hex_string(content)
	return content	

def generate_key_file(hex_path):
	hex_chars=check_content(hex_path)
	# print("hex_chars", hex_chars)
	fernet_key = Fernet.generate_key()
	obj_fernet = Fernet(fernet_key)
	encrypt_chars = obj_fernet.encrypt(hex_chars.encode())
	f = open("ft_opt.key", "wb")
	f.write(fernet_key)
	f.write(b"\n")
	f.write(encrypt_chars)
	f.close()
	print("the key file is generated!")


def check_key_file(encrypt_file):
	if not os.path.exists(encrypt_file):
		raise my_eception("Error :the {} file not be fond!".format(encrypt_file))
	file_name = os.path.basename(encrypt_file)
	if file_name != "ft_opt.key":
		raise my_eception("Error :the file name must be ft_opt.key!")
	with open(encrypt_file, "rb") as f:
		fernet_key= f.readline()
		encrypt_chars = f.readline()
		f.close()
	fernet = Fernet(fernet_key)
	hex_chars = fernet.decrypt(encrypt_chars)
	# print(hex_chars.decode())
	return hex_chars

def generate_hmac_num(decrypt_key, num):
	num_bytes = struct.pack('>Q', num)
	hmac_num = hmac.new(decrypt_key,num_bytes,hashlib.sha1).digest()
	return hmac_num

def truncate(hmac_digest):
	offset = hmac_digest[-1] & 0x0F 
	code_bytes = hmac_digest[offset:offset + 4]
	code = struct.unpack('>I',code_bytes)[0]
	code &= 0x7FFFFFFF # for positive integer
	code %= 10**6
	return code

def get_pass_word(decrypt_key):
	time_period = 60
	seed = int(time.time()/time_period)
	random.seed(seed)
	num = random.randint(100000,1000000)
	hmac_num=generate_hmac_num(decrypt_key, num)
	pass_word = truncate(hmac_num)
	print("one time password: {}".format(pass_word))

def generate_qr_code(key):
	qr = qrcode.QRCode(version=1,box_size=5, border=4)
	qr.add_data(key)
	qr.make(fit=True)
	qr_img = qr.make_image(fill="black", back_color="white")
	qr_img.save(QR_CODE_FILE)
	print("{} is saved".format(QR_CODE_FILE))



def main():
	try: 
		# hex_chars=get_check_file()
		# print(hex_chars)
		if len(sys.argv) != 3:
			raise my_eception("Error: you have to enter a flag and valid path for it!")
		elif sys.argv[1] == "-g" and len(sys.argv) == 3:
			generate_key_file(sys.argv[2])
		elif sys.argv[1] == "-k" and len(sys.argv) == 3:
			decrypt_key = check_key_file(sys.argv[2])
			get_pass_word(decrypt_key)
			generate_qr_code(decrypt_key.decode())
		else:
			raise my_eception("Error: you have to use one of the two flags '-g' or '-k' and give a valid file path!")

	except my_eception as e:
		print(str(e))

main()
