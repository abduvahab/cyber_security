# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_opt.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: areheman <areheman@student.42mulhouse.fr>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/25 16:14:11 by areheman          #+#    #+#              #
#    Updated: 2023/05/26 11:14:51 by areheman         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



import tkinter as tk
from tkinter import font
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
from PIL import Image, ImageTk


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
	return pass_word


def generate_qr_code(key):
	qr = qrcode.QRCode(version=1,box_size=5, border=4)
	qr.add_data(key)
	qr.make(fit=True)
	qr_img = qr.make_image(fill="black", back_color="white")
	qr_img.save(QR_CODE_FILE)
	# print("{} is saved".format(QR_CODE_FILE))

def draw_window():


	def get_hex_path():
		value_ent =  entry.get().strip()
		# print(value_ent, len(value_ent))
		try:
			hex_chars=check_content(value_ent)
			fernet_key = Fernet.generate_key()
			obj_fernet = Fernet(fernet_key)
			encrypt_chars = obj_fernet.encrypt(hex_chars.encode())
			f = open("ft_opt.key", "wb")
			f.write(fernet_key)
			f.write(b"\n")
			f.write(encrypt_chars)
			f.close()
			m_label["fg"]="blue"
			m_label["text"] = "ft_opt.key has been created!"
			entry.delete(0, tk.END)
		except Exception as err:
			m_label["fg"]="red"
			m_label["text"] = str(err)

		
	win = tk.Tk()
	win.title("HOTP Window")
	win.resizable(width=False,height=False)
	win.rowconfigure(0,minsize=50)
	win.rowconfigure(1,minsize=50)
	win.rowconfigure(2,minsize=50)
	win.columnconfigure(0,minsize=75)

	f_path = tk.Frame(width=100)
	f_path.pack()
	label_path= tk.Label(master=f_path,text="path:", relief=tk.FLAT)
	entry = tk.Entry(master=f_path, relief=tk.SUNKEN,width=60)
	b_key= tk.Button(master=f_path, relief=tk.SUNKEN, text="key", command=get_hex_path)
	label_path.grid(row=0,column=0,sticky='e')
	entry.grid(row=0,column=1,sticky='w')
	b_key.grid(row=0,column=2,sticky='w')
	m_label = tk.Label(master=f_path,text="", relief=tk.FLAT)
	m_label.grid(row=1,column=1)


#  frame for hotp and qr code 

	p_show = tk.Frame(height=300,width=100, relief=tk.RAISED, borderwidth=2)
	p_show.pack(fill=tk.BOTH,expand=True)
	p_show.rowconfigure(0,minsize=300)
	p_show.columnconfigure(0,minsize=300)
	p_show.columnconfigure(1,minsize=300)

	tk_images =None
	def get_password():
		encrypt_file="ft_opt.key"
		if not os.path.exists(encrypt_file):
			p_lable["font"] = font.Font(size=20)
			p_lable["fg"] = "red"
			p_lable["text"] = "No Key File"
			qr_lable["font"] = font.Font(size=20)
			qr_lable["fg"] = "red"
			qr_lable["text"] = "No Key File"
		else:
			with open(encrypt_file, "rb") as f:
				fernet_key= f.readline()
				encrypt_chars = f.readline()
				f.close()
			fernet = Fernet(fernet_key)
			hex_chars = fernet.decrypt(encrypt_chars)
			password=get_pass_word(hex_chars)
			p_lable["font"] = font.Font(size=50)
			p_lable["fg"] = "blue"
			p_lable["text"] = password
			generate_qr_code(hex_chars.decode())
			qr_lable["text"] = ""
			qr_image = Image.open(QR_CODE_FILE)
			qr_image=qr_image.resize((300,300))
			tk_images = ImageTk.PhotoImage(image=qr_image)
			qr_lable.config(image=tk_images)
			qr_lable.image= tk_images

	p_lable = tk.Label(master=p_show,text="", relief=tk.RAISED,borderwidth=2)
	p_lable.grid(row=0,column=0,sticky='wesn')
	
	
	qr_lable = tk.Label(master=p_show,image=tk_images, relief=tk.FLAT)
	qr_lable.grid(row=0,column=1)
	
#  get pass word bottom frame 
	f_get=tk.Frame(width=100,height=100,borderwidth=2, relief=tk.RAISED)
	f_get.pack(fill=tk.BOTH, expand=True)
	b_get=tk.Button(master=f_get, relief=tk.RAISED, text="Pass Word", command=get_password)
	b_get.pack(padx=5,pady=5)

	

	win.mainloop()

draw_window()