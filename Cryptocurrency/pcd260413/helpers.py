from hashlib import sha256
from datetime import datetime


def hash256(byte_string):
    return sha256(sha256(byte_string).digest()).digest()
    
def now():
    return int(datetime.now().timestamp()).to_bytes(4, 'big')

