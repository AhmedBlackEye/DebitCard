import cryptography.fernet


def encrypt_(msg, key=b'3gZ2d7Hz2cJXxOTJEsekj1dAB2l9Y8zGmVQp1cne_d8='):
    f = cryptography.fernet.Fernet(key)
    return f.encrypt(msg.encode())


def decrypt_(msg, key=b'3gZ2d7Hz2cJXxOTJEsekj1dAB2l9Y8zGmVQp1cne_d8='):
    f = cryptography.fernet.Fernet(key)
    msg = msg.encode()
    return f.decrypt(msg).decode()
