import base64
import os
from Crypto.Cipher import AES
from Crypto import Random

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

password_provided = "password" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=salt,
	iterations=100000,
	backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

#key = 'A'*32
#iv = "B"*16
# print(key)

file = open('key.key', 'wb')
file.write(key) # The key is type bytes still
file.close()

msg = 'this is secure'
def enc(msg):
	file = open('key.key', 'rb')
	key = file.read() # The key will be type bytes
	file.close()
	encoded = msg.encode()
	f = Fernet(key)
	encrypted = f.encrypt(encoded)
	print(encrypted)

def dec(msg):
	file = open('key.key', 'rb')
	key = file.read() # The key will be type bytes
	file.close()
	encoded = msg.encode()
	f = Fernet(key1)
	encrypted = f.encrypt(encoded)
	decrypted = f.decrypt(encrypted)
	print(decrypted)

with open('file.txt', 'rb') as f: # file
	data = f.read()
	

def enc_file(data): # what file u want to send
	fernet = Fernet(key)
	encrypted = fernet.encrypt(data)
	with open('file.txt.enc', 'wb') as f:
		f.write(encrypted)

with open('file.txt.enc', 'rb') as f: # encrypted file
	data1 = f.read()

def dec_file(data1): # decrypting the file
	fernet = Fernet(key)
	encrypted = fernet.decrypt(data1)
	with open('file.txt.dec', 'wb') as f:
		f.write(encrypted)

def rsa_key():
	key = RSA.generate(4096)
	f = open('./rsa_public.pem', 'wb')
	f.write(key.publickey().exportKey('PEM'))
	f.close()
	f = open('./rsa_private.pem', 'wb')
	f.write(key.exportKey('PEM'))
	f.close()

def rsa_enc():
	f = open('./rsa_public.pem', 'rb')
	key = RSA.importKey(f.read())
	x = key.encrypt(b"dddddd",32)
	print(x)
	return x
	
def rsa_dec():
	f1 = open('./sa_private.pem', 'rb')
	key1 = RSA.importKey(f1.read())
	z = key1.decrypt(x)
	print(z)
	return z

'''
input_file = open("photo.jpg", 'rb')
input_data = input_file.read()
input_file.close()


#def enc_file(input_data):
cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
enc_data = cfb_cipher.encrypt(input_data)

enc_file = open("encrypted.enc", "wb")
enc_file.write(enc_data)
enc_file.close()
'''

enc(msg)
dec(msg)
enc_file(data)
dec_file(data1)
rsa()

