'''
from Crypto.Cipher import AES
import base64

# the 'key' and the 'iv' is taken from the terminal after running aes_test.py
# key = 'gKdldH6lj9gEtb59Cr9lSsWNv7xFo5yr'
# iv = 'qUDmobVJ1vOGTvmS'

# def dec(data):
key = 'a'*32;
iv = 'b'*16;
enc_s = AES.new(key, AES.MODE_CFB, iv)
cipher_text = enc_s.encrypt("secret") 
encoded_cipher_text = base64.b64encode(cipher_text)

decryption_suite = AES.new(key, AES.MODE_CFB, iv)
plain_text = decryption_suite.decrypt(base64.b64decode(encoded_cipher_text))
	# return plain_text
print(plain_text)
'''
'''
import pyAesCrypt
from os import stat, remove
# encryption/decryption buffer size
bufferSize = 64 * 1024
password = 'pwd'# encryption of file data.txt
with open('photo.jpg', 'rb') as fIn:
	with open('photo.jpg.aes', 'wb') as fOut:
		pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)# get encrypted file size
		encFileSize = stat('photo.jpg.aes').st_size
		print(encFileSize) #prints file size# decryption of file data.aes

with open('photo.jpg.aes', 'rb') as fIn:
	with open('photo_out.jpg', 'wb') as fOut:
		try:
			# decrypt file stream
			pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
		except ValueError:
			# remove output file on error
			remove('photo_out.txt')
'''
'''
fo = open('hostx.jpg', 'rb')
image = fo.read()
fo.close()

image = bytearray(image)
key = 32

for index, value in enumerate(image):
	image[index] = value^key

fo = open('hostx_enc.jpg', 'wb')
fo.write(image)
fo.close()
'''
fo = open('hostx_dec.jpg', 'rb')
image = fo.read()
fo.close()

image = bytearray(image)
key = 32

for index, value in enumerate(image):
	image[index] = value^key

fo = open('hostx_re.jpg', 'wb')
fo.write(image)
fo.close()
