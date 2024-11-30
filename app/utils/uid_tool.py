import string
import secrets
def get_uid(length:int=12)->str:
        ''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(length))