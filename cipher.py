import cryptography.fernet

class cipher:
    def encrypt_msg(self, msg, key=b'3gZ2d7Hz2cJXxOTJEsekj1dAB2l9Y8zGmVQp1cne_d8='):
        f = cryptography.fernet.Fernet(key)
        return f.encrypt(msg.encode())

    def decrypt_msg(self, msg, key=b'3gZ2d7Hz2cJXxOTJEsekj1dAB2l9Y8zGmVQp1cne_d8='):
        f = cryptography.fernet.Fernet(key)
        return f.decrypt(msg).decode()

# msg = '1252'
# x = cipher().encrypt(msg)
# print(x.decode())