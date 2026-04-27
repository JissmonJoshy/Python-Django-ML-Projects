from cryptography.fernet import Fernet

SECRET_KEY = b'K4phJ_j7A9i-rlu_eOSt0PLvCq3_bId9EItJLhfW4uc='

cipher = Fernet(SECRET_KEY)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher.decrypt(data.encode()).decode()