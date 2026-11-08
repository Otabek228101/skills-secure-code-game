import secrets
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
        return bcrypt.hashpw(password.encode(), salt).decode('ascii')

    def password_verification(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash.encode('ascii'))

class MD5_hasher:

    def password_hash(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('ascii')

    def password_verification(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash.encode('ascii'))

PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'SHA256_hasher'
