import binascii
import secrets
import hashlib
import os
import bcrypt

class Random_generator:

    def generate_token(self, length=8, alphabet=(
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        return ''.join(secrets.choice(alphabet) for i in range(length))

    def generate_salt(self, rounds=12):
        return bcrypt.gensalt(rounds)

class SHA256_hasher:

    def password_hash(self, password, salt):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = bcrypt.hashpw(password, salt)
        return password_hash.decode('ascii')

    def password_verification(self, password, password_hash):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = password_hash.encode('ascii')
        return bcrypt.checkpw(password, password_hash)

class MD5_hasher:

    def password_hash(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def password_verification(self, password, password_hash):
        password = self.password_hash(password)
        return secrets.compare_digest(password.encode(), password_hash.encode())
    
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'SHA256_hasher'
