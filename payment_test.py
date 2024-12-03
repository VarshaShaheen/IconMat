import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# AES Key (16 bytes for AES-128)
AES_KEY = b"1400012609205020"  # Replace with your encryption key


def encrypt_data(data):
	"""Encrypt data using AES ECB mode with PKCS7 padding."""
	# No need to hash the key, use it directly for AES-128
	key = AES_KEY  # AES requires a 16-byte key

	# Convert data to bytes
	data_bytes = data.encode('utf-8')

	# Create AES cipher instance with ECB mode
	cipher = AES.new(key, AES.MODE_ECB)

	# Apply PKCS7 padding to the data
	padded_data = pad(data_bytes, AES.block_size)

	# Encrypt the padded data
	encrypted = cipher.encrypt(padded_data)

	# Encode the encrypted data in base64 and return
	return base64.b64encode(encrypted).decode('utf-8')


def prepare_encrypted_link():
	# Data to be encrypted
	fields_to_encrypt = {
		"mandatoryfields"  : "1023abcde|45|10000|26/NOV/2024",
		"optionalfields"   : "x|test@gmail.com|9876543210|x|x",
		"returnurl"        : "http://localhost:8000/payment/process/",
		"ReferenceNo"      : "1023abcde",
		"submerchantid"    : "45",
		"transactionamount": "10000",
		"paymode"          : "9"
	}

	# Encrypt the data
	encrypted_fields = {key: encrypt_data(value) for key, value in fields_to_encrypt.items()}

	# Construct the encrypted URL
	encrypted_url = (
		f"https://eazypay.icicibank.com/EazyPG?"
		f"merchantid=140921&"  # Non-encrypted merchantid
		f"mandatoryfields={encrypted_fields['mandatoryfields']}&"
		f"optionalfields={encrypted_fields['optionalfields']}&"
		f"returnurl={encrypted_fields['returnurl']}&"
		f"ReferenceNo={encrypted_fields['ReferenceNo']}&"
		f"submerchantid={encrypted_fields['submerchantid']}&"
		f"transactionamount={encrypted_fields['transactionamount']}&"
		f"paymode={encrypted_fields['paymode']}"
	)

	return encrypted_url


# Get the encrypted URL
encrypted_url = prepare_encrypted_link()

# Print the encrypted URL
print("Encrypted URL:")
print(encrypted_url)
